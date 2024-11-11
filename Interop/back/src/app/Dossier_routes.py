import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.database import get_db
from src.model.Dossier import DossierMedical, CompteRenduMedical
from src.schemas.DossierSchema import DossierMedicalSchema, CompteRenduMedicalSchema

logger = logging.getLogger('uvicorn.error')

router = APIRouter()

class CreateMedicalReportSchema(BaseModel):
    patient_id: int
    title: str
    content: str

    class Config:
        orm_mode = True


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
async def create_medical_report(patient_id: int, report: CreateMedicalReportSchema, db: Session = Depends(get_db)):
    dossier_medical = db.query(DossierMedical).filter(DossierMedical.patient_id == patient_id).first()

    if not dossier_medical:
        raise HTTPException(status_code=404, detail="Dossier médical non trouvé pour ce patient")

    # Créer un nouveau rapport médical associé au dossier médical existant
    new_report = CompteRenduMedical(
        dossier_medical_id=dossier_medical.id,  # Associer le rapport au dossier médical
        title=report.title,
        content=report.content
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report


@router.patch("/{patient_id}/reports/{report_id}", response_model=CompteRenduMedicalSchema)
async def update_medical_report(patient_id: int, report_id: int, report: CreateMedicalReportSchema,
                                db: Session = Depends(get_db)):
    db_report = db.query(CompteRenduMedical).filter(
        CompteRenduMedical.id == report_id,
        CompteRenduMedical.patient_id == patient_id
    ).first()

    if not db_report:
        raise HTTPException(status_code=404, detail="Medical report not found")

    db_report.title = report.title
    db_report.content = report.content
    db.commit()
    db.refresh(db_report)
    return db_report

# Route pour supprimer un rapport médical d'un patient
@router.delete("/{patient_id}/reports/{report_id}")
async def delete_medical_report(patient_id: int, report_id: int, db: Session = Depends(get_db)):
    db_report = db.query(CompteRenduMedical).filter(
        CompteRenduMedical.id == report_id,
        CompteRenduMedical.patient_id == patient_id
    ).first()

    if not db_report:
        raise HTTPException(status_code=404, detail="Medical report not found")

    db.delete(db_report)
    db.commit()
    return {"message": "Medical report deleted successfully"}

# Route pour obtenir tous les dossiers médicaux d'un patient
@router.get("/{patient_id}/dossier", response_model=List[DossierMedicalSchema])
async def get_dossier_medical(patient_id: int, db: Session = Depends(get_db)):
    dossiers = db.query(DossierMedical).filter(DossierMedical.patient_id == patient_id).all()
    return dossiers
