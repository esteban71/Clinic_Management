import logging
from datetime import datetime, timedelta

import fhirclient.models.patient as fhir_patient
import numpy as np
from faker import Faker
from fhirclient.models.address import Address
from fhirclient.models.attachment import Attachment
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.device import Device, DeviceDeviceName
from fhirclient.models.documentreference import DocumentReference, DocumentReferenceContent
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.fhirdatetime import FHIRDateTime
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.humanname import HumanName
from fhirclient.models.identifier import Identifier
from fhirclient.models.observation import Observation as FHIRObservation, ObservationComponent
from fhirclient.models.quantity import Quantity
from sqlalchemy.orm import Session
from src.model.DispositifMedicaux import DispositifMedicaux
from src.model.Dossier import DossierMedical
from src.model.Observation import Observation
from src.model.Patient import Patient
from src.utils.FHIR import smart_request as smart

fake = Faker()

logger = logging.getLogger('uvicorn.error')


def create_medical_folder(db: Session, patient_id: int):
    dossier = DossierMedical(
        patient_id=patient_id,
        date_creation=fake.date_of_birth(),
        type_acces=fake.random_element(elements=("public", "private"))
    )
    return dossier


def create_dispositif_medical(db: Session, patient_id: list[int] | int):
    if isinstance(patient_id, int):
        patient_id = [patient_id]
    dispositifs = []
    for i in patient_id:
        dispositif = DispositifMedicaux(
            patient_id=i,
            name=fake.name(),
            type=fake.random_element(
                elements=("Blood Pressure Monitor", "Heart Rate Monitor", "Oxygen Saturation Monitor")),
            interval=fake.random_int(min=1, max=30),
            status="active",
            manufacturer=fake.company(),
            serial_number=fake.random_int(min=1, max=1000),
            lot_number=fake.random_int(min=1, max=1000),
            manufacture_date=fake.date_of_birth(),
            expiration_date=fake.date_of_birth()
        )
        db.add(dispositif)
        db.commit()
        db.refresh(dispositif)
        dispositifs.append(dispositif)
        new_dispositif = dispositif
        try:
            device = Device()

            device_name = DeviceDeviceName()
            device_name.name = new_dispositif.name
            device_name.type = "user-friendly-name"
            device.deviceName = [device_name]

            codeable_concept = CodeableConcept()
            codeable_concept.text = new_dispositif.type
            device.type = codeable_concept

            device.status = new_dispositif.status.lower()

            device.manufacturer = new_dispositif.manufacturer

            device.serialNumber = new_dispositif.serial_number
            device.lotNumber = new_dispositif.lot_number

            device.manufactureDate = FHIRDateTime(new_dispositif.manufacture_date.isoformat())
            device.expirationDate = FHIRDateTime(new_dispositif.expiration_date.isoformat())
            identifier = Identifier()
            identifier.system = "backend"
            identifier.value = str(new_dispositif.id)
            device.identifier = [identifier]

            identifier_system = "backend"
            identifier_value = i

            search_resource = fhir_patient.Patient.where(
                struct={"identifier": f"{identifier_system}|{identifier_value}"}).perform(
                smart().server)

            fhir_patient_resource = fhir_patient.Patient.read(search_resource.entry[0].resource.id, smart().server)

            device.patient = FHIRReference({"reference": f"Patient/{fhir_patient_resource.id}"})

            device.create(smart().server)
        except Exception as e:
            logger.error(f"Error creating device: {e}")
            continue

    dispositif_ids = [dispositif.id for dispositif in dispositifs]
    return dispositif_ids


def add_observation_to_dispositif_heart(db: Session, dispositif_id: list[int] | int):
    if isinstance(dispositif_id, int):
        dispositif_id = [dispositif_id]
    for i in dispositif_id:
        dispositif = db.query(DispositifMedicaux).filter(DispositifMedicaux.id == i).first()
        ob = Observation(
            device_id=i,
            date_time=datetime.now() + timedelta(days=fake.random_int(min=-10, max=10)),
            code="Heart rate",
            value=fake.random_int(min=30, max=200),
            unit="bpm",
            device=dispositif
        )
        db.add(ob)
        db.commit()
        db.refresh(ob)
        new_observation = ob
        try:
            fhir_observation = FHIRObservation()
            fhir_observation.status = new_observation.status

            codeable_concept = CodeableConcept()
            codeable_concept.text = new_observation.code

            fhir_observation.code = codeable_concept

            search_device = Device.where(struct={"identifier": f"backend|{i}"}).perform(
                smart().server)

            device = Device.read(search_device.entry[0].resource.id, smart().server)
            fhir_observation.subject = FHIRReference({"reference": f"Device/{device.id}"})
            quantity = Quantity()
            quantity.value = new_observation.value
            quantity.unit = new_observation.unit
            fhir_observation.valueQuantity = quantity

            if new_observation.component_code:
                component_codeable_concept = CodeableConcept()
                component_codeable_concept.text = new_observation.component_code
                component = ObservationComponent()
                component.code = component_codeable_concept

                component_quantity = Quantity()
                component_quantity.value = new_observation.component_value
                component_quantity.unit = new_observation.component_unit
                component.valueQuantity = component_quantity

                fhir_observation.component = [component]

            fhir_observation.create(smart().server)

        except Exception as e:
            continue


def add_observation_to_dispositif_blood(db: Session, dispositif_id: list[int] | int):
    if isinstance(dispositif_id, int):
        dispositif_id = [dispositif_id]
    for i in dispositif_id:
        dispositif = db.query(DispositifMedicaux).filter(DispositifMedicaux.id == i).first()
        ob = Observation(
            device_id=i,
            status="final",
            date_time=datetime.now() + timedelta(days=fake.random_int(min=-10, max=10)),
            code="Blood pressure",
            value=fake.random_int(min=60, max=200),
            unit="mmHg",
            component_code=fake.random_element(elements=("systolic", "diastolic")),
            component_value=fake.random_int(min=60, max=200),
            component_unit="mmHg",
            device=dispositif
        )
        db.add(ob)
        db.commit()
        db.refresh(ob)
        new_observation = ob
        try:
            fhir_observation = FHIRObservation()
            fhir_observation.status = new_observation.status

            codeable_concept = CodeableConcept()
            codeable_concept.text = new_observation.code

            fhir_observation.code = codeable_concept

            search_device = Device.where(struct={"identifier": f"backend|{i}"}).perform(
                smart().server)

            device = Device.read(search_device.entry[0].resource.id, smart().server)
            fhir_observation.subject = FHIRReference({"reference": f"Device/{device.id}"})
            quantity = Quantity()
            quantity.value = new_observation.value
            quantity.unit = new_observation.unit
            fhir_observation.valueQuantity = quantity

            if new_observation.component_code:
                component_codeable_concept = CodeableConcept()
                component_codeable_concept.text = new_observation.component_code
                component = ObservationComponent()
                component.code = component_codeable_concept

                component_quantity = Quantity()
                component_quantity.value = new_observation.component_value
                component_quantity.unit = new_observation.component_unit
                component.valueQuantity = component_quantity

                fhir_observation.component = [component]

            fhir_observation.create(smart().server)

        except Exception as e:
            continue


def add_observation_to_dispositif_oxygen(db: Session, dispositif_id: list[int] | int):
    if isinstance(dispositif_id, int):
        dispositif_id = [dispositif_id]
    for i in dispositif_id:
        dispositif = db.query(DispositifMedicaux).filter(DispositifMedicaux.id == i).first()
        ob = Observation(
            device_id=i,
            date_time=datetime.now() + timedelta(days=fake.random_int(min=-10, max=10)),
            code="Oxygen saturation",
            value=fake.random_int(min=60, max=100),
            unit="%",
            device=dispositif
        )
        db.add(ob)
        db.commit()
        db.refresh(ob)
        new_observation = ob
        try:
            fhir_observation = FHIRObservation()
            fhir_observation.status = new_observation.status

            codeable_concept = CodeableConcept()
            codeable_concept.text = new_observation.code

            fhir_observation.code = codeable_concept

            search_device = Device.where(struct={"identifier": f"backend|{i}"}).perform(
                smart().server)

            device = Device.read(search_device.entry[0].resource.id, smart().server)
            fhir_observation.subject = FHIRReference({"reference": f"Device/{device.id}"})
            fhir_observation.effectiveDateTime = new_observation.date_time.isoformat()
            quantity = Quantity()
            quantity.value = new_observation.value
            quantity.unit = new_observation.unit
            fhir_observation.valueQuantity = quantity

            if new_observation.component_code:
                component_codeable_concept = CodeableConcept()
                component_codeable_concept.text = new_observation.component_code
                component = ObservationComponent()
                component.code = component_codeable_concept

                component_quantity = Quantity()
                component_quantity.value = new_observation.component_value
                component_quantity.unit = new_observation.component_unit
                component.valueQuantity = component_quantity

                fhir_observation.component = [component]

            fhir_observation.create(smart().server)

        except Exception as e:
            continue


def create_patient(db: Session, nb_patient: int):
    patient_ids = []
    dossiers = []
    patients = []

    for i in range(nb_patient):
        dossier_medical = create_medical_folder(db, i)

        dossiers.append(dossier_medical)  # Add to list

        patient = Patient(
            name=fake.name(),
            active=fake.boolean(),
            telecom=fake.phone_number(),
            gender=fake.random_element(elements=("male", "female")),
            birth_date=fake.date_of_birth(),
            address=fake.address(),
            marital_status=fake.random_element(elements=("single", "married", "divorced")),
            dossier_medical=dossier_medical
        )
        patients.append(patient)
        db.add(patient)
        db.add(dossier_medical)
        db.commit()
        db.refresh(patient)
        db.refresh(dossier_medical)
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
            fhir_patient_resource.birthDate = FHIRDate(patient.birth_date.isoformat()) if patient.birth_date else None

            # Add marital status (if available)
            if patient.marital_status:
                codeable_concept = CodeableConcept()
                codeable_concept.text = patient.marital_status
                fhir_patient_resource.maritalStatus = codeable_concept

            identifier = Identifier()
            identifier.system = "backend"
            identifier.value = str(patient.id)

            fhir_patient_resource.identifier = [
                identifier
            ]

            # Convert to JSON and log for debugging
            fhir_patient_json = fhir_patient_resource.as_json()

            fhir_patient_resource.create(smart().server)

            search_resource = fhir_patient.Patient.where(
                struct={"identifier": f"{identifier.system}|{identifier.value}"}).perform(
                smart().server)
            fhir_patient_resource_with_id = fhir_patient.Patient.read(search_resource.entry[0].resource.id,
                                                                      smart().server)

            fhir_document_reference = DocumentReference()
            identifier_document_reference = Identifier()
            identifier_document_reference.system = "backend"
            identifier_document_reference.value = str(dossier_medical.id)
            fhir_document_reference.identifier = [identifier_document_reference]
            fhir_document_reference.status = "current"
            fhir_document_reference.type = CodeableConcept({"text": "Dossier Medical"})
            fhir_document_reference.subject = FHIRReference(
                {"reference": f"Patient/{fhir_patient_resource_with_id.id}"})

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

        except Exception as e:
            continue

    patient_ids = [patient.id for patient in patients]
    db.refresh(patients[-1])
    db.refresh(dossiers[-1])
    return patient_ids


def add_medecin_to_patient(db: Session, medecin_id: list[int] | int, patient_id: list[int]):
    for i in range(len(patient_id)):
        patient = db.query(Patient).filter(Patient.id == patient_id[i]).first()
        if isinstance(medecin_id, int):
            patient.medecin_id = medecin_id
        else:
            random_medecin_id = int(np.random.choice(medecin_id))
            patient.medecin_id = random_medecin_id
    db.commit()
    db.refresh(patient)
