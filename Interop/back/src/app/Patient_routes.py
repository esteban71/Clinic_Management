from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import Patient
from src.schemas import PatientSchema
from typing import Dict, Any, List

router = APIRouter()


@router.get("/{patient_id}", response_model=PatientSchema)  # Added response_model
async def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.get("", response_model=List[PatientSchema])  # Added response_model
async def get_all_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()

    return patients


