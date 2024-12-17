import logging
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.database import get_db
from src.model.Dossier import DossierMedical, CompteRenduMedical
from src.schemas.DossierSchema import DossierMedicalSchema, CompteRenduMedicalSchema, CreateCompteRenduMedicalSchema
from fhirclient.models.documentreference import DocumentReference
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.identifier import Identifier
from fhirclient.models.coding import Coding
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.attachment import Attachment
from fhirclient.models.documentreference import DocumentReferenceContent
from src.utils.FHIR import smart_request as smart
from fhirclient.models.fhirdatetime import FHIRDateTime

logger = logging.getLogger('uvicorn.error')

router = APIRouter()


@router.get("/{patient_id}/reports", response_model=List[CompteRenduMedicalSchema])
async def get_medical_reports(patient_id: int, db: Session = Depends(get_db)):
    medical_reports = (
        db.query(CompteRenduMedical)
        .join(DossierMedical)
        .filter(DossierMedical.patient_id == patient_id)
        .all()
    )
    return medical_reports


@router.post("/{patient_id}/reports/new", response_model=CompteRenduMedicalSchema)
async def create_medical_report(request: Request, patient_id: int, report: CreateCompteRenduMedicalSchema,
                                db: Session = Depends(get_db)):
    medecin_id = None
    if request.state.user["attributes"].get("medecin_id") is not None:
        medecin_id = int(request.state.user["attributes"]["medecin_id"][0])
    dossier_medical = db.query(DossierMedical).filter(DossierMedical.patient_id == patient_id).first()

    if not dossier_medical:
        raise HTTPException(status_code=404, detail="Dossier médical non trouvé pour ce patient")

    # patient = db.query(Patient).filter(Patient.id == dossier_medical.patient_id).first()
    # medecin_id = medecin_id

    # Créer un nouveau rapport médical associé au dossier médical existant
    new_report = CompteRenduMedical(
        dossier_medical_id=dossier_medical.id,
        title=report.title,
        content=report.content,
        date=datetime.strptime(report.date, "%Y-%m-%d").date(),
        auteur_id=medecin_id if medecin_id else None
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    try:
        # Créer un document FHIR pour le rapport médical
        identifier_system = "backend"
        indentifier_value = dossier_medical.id
        document = DocumentReference.where(
            struct={"identifier": f"{identifier_system}|{indentifier_value}"}).perform(
            smart().server)
        if not document:
            return new_report
        document_reference = DocumentReference.read(document.entry[0].resource.id, smart().server)
        document_content = DocumentReferenceContent()
        attachment = Attachment()
        attachment.contentType = "text/plain"
        attachment.data = report.content
        attachment.title = report.title + " - " + str(new_report.id)
        attachment.creation = FHIRDateTime(report.date)

        document_content.attachment = attachment

        document_reference.content.append(document_content)

        if document_reference.author and medecin_id:
            document_reference.author.append(FHIRReference({"reference": f"Practitioner/{medecin_id}"}))
        elif medecin_id:
            document_reference.author = [FHIRReference({"reference": f"Practitioner/{medecin_id}"})]

        logger.info(f"Document reference: {document_reference.as_json()}")

        document_reference.update(smart().server)

    except Exception as e:
        logger.error(f"Error creating FHIR document: {e}")
        return new_report

    return new_report


@router.patch("/{patient_id}/reports/{report_id}", response_model=CompteRenduMedicalSchema)
async def update_medical_report(patient_id: int, report_id: int, report: CreateCompteRenduMedicalSchema,
                                db: Session = Depends(get_db)):
    db_report = db.query(CompteRenduMedical).filter(
        CompteRenduMedical.id == report_id
    ).first()

    if not db_report:
        raise HTTPException(status_code=404, detail="Medical report not found")

    db_report.title = report.title
    db_report.content = report.content
    db.commit()
    db.refresh(db_report)

    dossier_medical = db.query(DossierMedical).filter(DossierMedical.patient_id == patient_id).first()

    try:

        identifier_system = "backend"
        indentifier_value = dossier_medical.id
        document = DocumentReference.where(
            struct={"identifier": f"{identifier_system}|{indentifier_value}"}).perform(
            smart().server)
        if not document:
            return db_report
        document_reference = DocumentReference.read(document.entry[0].resource.id, smart().server)
        document_content = DocumentReferenceContent()
        attachment = Attachment()
        attachment.contentType = "text/plain"
        attachment.data = report.content
        attachment.title = report.title + " - " + str(db_report.id)
        attachment.creation = FHIRDateTime(report.date)

        document_content.attachment = attachment

        # find the document content to update
        for content in document_reference.content:
            split_title = content.attachment.title.split(" - ")
            if len(split_title) > 1 and split_title[1] == str(report_id):
                content.attachment = attachment
                break

        document_reference.update(smart().server)

    except Exception as e:
        logger.error(f"Error creating FHIR document: {e}")
        return db_report
    return db_report


# Route pour supprimer un rapport médical d'un patient
@router.delete("/{patient_id}/reports/{report_id}")
async def delete_medical_report(patient_id: int, report_id: int, db: Session = Depends(get_db)):
    db_report = db.query(CompteRenduMedical).filter(
        CompteRenduMedical.id == report_id,
    ).first()

    if not db_report:
        raise HTTPException(status_code=404, detail="Medical report not found")

    db.delete(db_report)
    db.commit()
    dossier_medical = db.query(DossierMedical).filter(DossierMedical.patient_id == patient_id).first()
    try:
        # Supprimer le document FHIR associé au rapport médical
        identifier_system = "backend"
        indentifier_value = dossier_medical.id
        document = DocumentReference.where(
            struct={"identifier": f"{identifier_system}|{indentifier_value}"}).perform(
            smart().server)
        if not document:
            return {"message": "Medical report deleted successfully"}
        document_reference = DocumentReference.read(document.entry[0].resource.id, smart().server)

        for content in document_reference.content:
            split_title = content.attachment.title.split(" - ")
            if len(split_title) > 1 and split_title[1] == str(report_id):
                document_reference.content.remove(content)
                break

        document_reference.update(smart().server)
    except Exception as e:
        logger.error(f"Error deleting FHIR document: {e}")
        return {"message": "Medical report deleted successfully"}
    return {"message": "Medical report deleted successfully"}


# Route pour obtenir tous les dossiers médicaux d'un patient
@router.get("/{patient_id}/dossier", response_model=List[DossierMedicalSchema])
async def get_dossier_medical(patient_id: int, db: Session = Depends(get_db)):
    dossiers = db.query(DossierMedical).filter(DossierMedical.patient_id == patient_id).all()
    return dossiers
