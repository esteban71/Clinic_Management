import logging
from typing import Dict, List

import fhirclient.models.patient as fhir_patient
import fhirclient.models.practitioner as fhir_practitioner
from fastapi import APIRouter, Depends, HTTPException, Request
from fhirclient.models.address import Address
from fhirclient.models.attachment import Attachment
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.documentreference import DocumentReference
from fhirclient.models.documentreference import DocumentReferenceContent
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.humanname import HumanName
from fhirclient.models.identifier import Identifier
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import Patient, Medecin, DossierMedical
from src.schemas import PatientSchema
from src.schemas.PatientSchema import CreatePatientSchema
from src.utils.FHIR import add_practitioner_to_patient
from src.utils.FHIR import smart_request as smart

logger = logging.getLogger('uvicorn.error')

router = APIRouter()


@router.get("", response_model=List[PatientSchema])  # Added response_model
async def get_all_patients(request: Request, db: Session = Depends(get_db)):
    if request.state.user["attributes"].get("medecin_id") is not None:
        medecin_id = int(request.state.user["attributes"]["medecin_id"][0])
        logger.info(f"Getting patient with id {medecin_id}")
        patients = db.query(Patient).filter(Patient.medecin_id == medecin_id).all()
        if patients is None:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patients
    if request.state.user["attributes"].get("cabinet_id") is not None:
        cabinet_id = int(request.state.user["attributes"]["cabinet_id"][0])
        logger.info(f"Getting patient with id {cabinet_id}")
        patients = db.query(Patient).filter(Patient.cabinet_medical_id == cabinet_id).all()
        if patients is None:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patients
    patients = db.query(Patient).all()

    return patients


@router.post("", response_model=PatientSchema)
async def create_patient(patient: CreatePatientSchema,
                         db: Session = Depends(get_db)):
    # check if patient exists
    db_patient = db.query(Patient).filter(Patient.name == patient.name).first()
    if db_patient is not None:
        raise HTTPException(status_code=400, detail="Patient already exists")
    cabinet_id = db.query(Medecin).filter(Medecin.id == patient.medecin_id).first().cabinet_medical_id
    db_patient = Patient(
        name=patient.name,
        telecom=patient.telecom,
        address=patient.address,
        email=patient.email,
        medecin_id=patient.medecin_id,
        cabinet_medical_id=cabinet_id
    )
    db.add(db_patient)
    db.commit()
    db_dossier_medical = DossierMedical(
        patient_id=db_patient.id,
    )
    db.add(db_dossier_medical)
    db.commit()
    db.refresh(db_patient)
    db.refresh(db_dossier_medical)

    try:
        # Create FHIR Patient resource
        fhir_patient_resource = fhir_patient.Patient()
        name = HumanName()
        name.given = [str(patient.name)]  # Ensure it is a string
        name.family = ""  # Add family name for completeness (modify as needed)

        # Assign name to Patient resource
        fhir_patient_resource.name = [name]

        # Construct telecom (phone)
        contact_point = ContactPoint()
        contact_point.system = "phone"  # Specify the telecom system (e.g., phone, email)
        contact_point.value = patient.telecom  # Ensure it's a string
        contact_point.use = "home"  # Optional, but good practice

        contact_point2 = ContactPoint()
        contact_point2.system = "email"  # Specify the telecom system (e.g., phone, email)
        contact_point2.value = patient.email  # Ensure it's a string
        contact_point2.use = "home"  # Optional, but good practice

        fhir_patient_resource.telecom = [contact_point, contact_point2]

        # Construct address
        address = Address()
        address.line = [str(patient.address)]  # Use line instead of text for better structure
        address.city = ""  # Add city, postal code, country (modify as needed)
        address.postalCode = ""
        address.country = ""

        fhir_patient_resource.address = [address]

        # Assign gender and birthDate
        fhir_patient_resource.gender = patient.gender if patient.gender else None
        fhir_patient_resource.birthDate = patient.birth_date.isoformat() if patient.birth_date else None

        # Add marital status (if available)
        if patient.marital_status:
            codeable_concept = CodeableConcept()
            codeable_concept.text = patient.marital_status
            fhir_patient_resource.maritalStatus = codeable_concept

        identifier = Identifier()
        identifier.system = "backend"
        identifier.value = str(db_patient.id)

        fhir_patient_resource.identifier = [
            identifier
        ]

        # Convert to JSON and log for debugging
        fhir_patient_json = fhir_patient_resource.as_json()
        logger.error(f"FHIR Patient JSON: {fhir_patient_json}")

        fhir_patient_resource.create(smart().server)

        search_resource = fhir_patient.Patient.where(
            struct={"identifier": f"{identifier.system}|{identifier.value}"}).perform(
            smart().server)
        fhir_patient_resource_with_id = fhir_patient.Patient.read(search_resource.entry[0].resource.id, smart().server)

        fhir_document_reference = DocumentReference()
        identifier_document_reference = Identifier()
        identifier_document_reference.system = "backend"
        identifier_document_reference.value = str(db_dossier_medical.id)
        fhir_document_reference.identifier = [identifier_document_reference]
        fhir_document_reference.status = "current"
        fhir_document_reference.type = CodeableConcept({"text": "Dossier Medical"})
        fhir_document_reference.subject = FHIRReference({"reference": f"Patient/{fhir_patient_resource_with_id.id}"})

        DocumentReference_content = DocumentReferenceContent()
        attachment = Attachment()
        attachment.contentType = "application/json"
        attachment.data = "string"
        attachment.title = "Dossier Medical"

        DocumentReference_content.attachment = attachment

        fhir_document_reference.content = [DocumentReference_content]

        fhir_document_reference.create(smart().server)

        # Add DocumentReference to Patient resource
        fhir_patient_resource_with_id.contained = [fhir_document_reference]

        fhir_patient_resource_with_id.update(smart().server)

        try:
            identifier_system = "backend"
            identifier_value_medecin = str(patient.medecin_id)
            search_resource_medecin = fhir_practitioner.Practitioner.where(
                struct={"identifier": f"{identifier_system}|{identifier_value_medecin}"}).perform(
                smart().server)
            identifier_system = "backend"
            identifier_value = str(db_patient.id)
            search_resource_patient = fhir_patient.Patient.where(
                struct={"identifier": f"{identifier_system}|{identifier_value}"}).perform(
                smart().server)
            add_practitioner_to_patient(search_resource_patient, search_resource_medecin.entry[0].resource.id)
        except Exception as e:
            logger.info(f"Error adding practitioner to patient: {e}")
            return db_patient

    except Exception as e:
        logger.info(f"Error creating FHIR Patient resource: {e}")
        return db_patient

    return db_patient


@router.patch("", response_model=PatientSchema)
async def update_patient(patient: PatientSchema, db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.id == patient.id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    db_patient.name = patient.name
    db_patient.telecom = patient.telecom
    db_patient.address = patient.address
    db_patient.email = patient.email
    if patient.medecin_id is not None:
        cabinet_id = db.query(Medecin).filter(Medecin.id == patient.medecin_id).first().cabinet_medical_id
        db_patient.medecin_id = patient.medecin_id
        db_patient.cabinet_medical_id = cabinet_id
    db.commit()
    db.refresh(db_patient)

    # Update FHIR Patient resource
    identifier_system = "backend"
    identifier_value = str(db_patient.id)
    try:
        # Perform a search for the Patient resource by identifier
        search_resource = fhir_patient.Patient.where(
            struct={"identifier": f"{identifier_system}|{identifier_value}"}).perform(
            smart().server)
        if search_resource is None:
            return db_patient
        fhir_patient_resource = fhir_patient.Patient.read(search_resource.entry[0].resource.id, smart().server)
        fhir_patient_resource.id = fhir_patient_resource.id
        name = HumanName()
        name.given = [str(patient.name)]  # Ensure it is a string
        name.family = ""  # Add family name for completeness (modify as needed)

        # Assign name to Patient resource
        fhir_patient_resource.name = [name]

        # Construct telecom (phone)
        contact_point = ContactPoint()
        contact_point.system = "phone"  # Specify the telecom system (e.g., phone, email)
        contact_point.value = patient.telecom  # Ensure it's a string
        contact_point.use = "home"  # Optional, but good practice

        contact_point2 = ContactPoint()
        contact_point2.system = "email"  # Specify the telecom system (e.g., phone, email)
        contact_point2.value = patient.email  # Ensure it's a string
        contact_point2.use = "home"  # Optional, but good practice

        fhir_patient_resource.telecom = [contact_point, contact_point2]

        # Construct address
        address = Address()
        address.line = [str(patient.address)]  # Use line instead of text for better structure
        address.city = ""  # Add city, postal code, country (modify as needed)
        address.postalCode = ""
        address.country = ""

        fhir_patient_resource.address = [address]

        # Assign gender and birthDate
        fhir_patient_resource.gender = patient.gender if patient.gender else None
        fhir_patient_resource.birthDate = patient.birth_date.isoformat() if patient.birth_date else None

        # Add marital status (if available)
        if patient.marital_status:
            codeable_concept = CodeableConcept()
            codeable_concept.text = patient.marital_status
            fhir_patient_resource.maritalStatus = codeable_concept

        # Convert to JSON and log for debugging
        fhir_patient_json = fhir_patient_resource.as_json()
        logger.error(f"FHIR Patient JSON: {fhir_patient_json}")

        fhir_patient_resource.update(smart().server)

        if patient.medecin_id is not None:
            try:
                identifier_system = "backend"
                identifier_value_medecin = str(patient.medecin_id)
                search_resource_medecin = fhir_practitioner.Practitioner.where(
                    struct={"identifier": f"{identifier_system}|{identifier_value_medecin}"}).perform(
                    smart().server)
                identifier_system = "backend"
                identifier_value = str(db_patient.id)
                search_resource_patient = fhir_patient.Patient.where(
                    struct={"identifier": f"{identifier_system}|{identifier_value}"}).perform(
                    smart().server)
                add_practitioner_to_patient(search_resource_patient, search_resource_medecin.entry[0].resource.id)
            except Exception as e:
                logger.info(f"Error adding practitioner to patient: {e}")
                return db_patient

    except Exception as e:
        logger.info(f"Error updating FHIR Patient resource: {e}")
        return db_patient

    return db_patient


@router.delete("")
def delete_patient(patient_id: Dict[str, int], db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.id == patient_id['id']).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(db_patient)
    db.commit()

    identifier_system = "backend"
    identifier_value = str(db_patient.id)

    try:
        # Perform a search for the Patient resource by identifier
        search_resource = fhir_patient.Patient.where(
            struct={"identifier": f"{identifier_system}|{identifier_value}"}).perform(
            smart().server)
        if search_resource is None:
            return {"message": "Patient deleted successfully but FHIR resource not found"}
        fhir_patient_resource = fhir_patient.Patient.read(search_resource.entry[0].resource.id, smart().server)
        fhir_patient_resource.id = fhir_patient_resource.id
        fhir_patient_resource.delete(smart().server)
    except Exception as e:
        logger.info(f"Error deleting FHIR Patient resource: {e}")
        return {"message": f"Patient deleted successfully but FHIR resource not found: {e}"}

    return {"message": "Patient deleted successfully"}
