import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.database import get_db
from src.model.Dossier import DossierMedical
from src.schemas.DossierSchema import DossierMedicalSchema
from datetime import date

logger = logging.getLogger('uvicorn.error')

router = APIRouter()


@router.get("", response_model=List[DossierMedicalSchema])
async def get_all_dossiers(db: Session = Depends(get_db)):
    dossiers = db.query(DossierMedical).all()
    return dossiers


class CreateDossierMedicalSchema(BaseModel):
    patient_id: int
    date_creation: date
    type_acces: str
    cabinet_medical_id: int

    class Config:
        orm_mode = True


@router.post("")
async def create_dossier(dossier: CreateDossierMedicalSchema, db: Session = Depends(get_db)):
    db_dossier = db.query(DossierMedical).filter(
        DossierMedical.patient_id == dossier.patient_id,
        DossierMedical.cabinet_medical_id == dossier.cabinet_medical_id
    ).first()
    
    if db_dossier is not None:
        raise HTTPException(status_code=400, detail="Dossier already exists for this patient and cabinet")

    new_dossier = DossierMedical(
        patient_id=dossier.patient_id,
        date_creation=dossier.date_creation,
        type_acces=dossier.type_acces,
        cabinet_medical_id=dossier.cabinet_medical_id
    )

    db.add(new_dossier)
    db.commit()
    db.refresh(new_dossier)
    return new_dossier
