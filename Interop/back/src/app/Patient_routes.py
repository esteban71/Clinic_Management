from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import Patient
from src.schemas import PatientSchema, CreatePatientSchema
from typing import Dict, List
import logging

from src.schemas.PatientSchema import CreatePatientSchema

logger = logging.getLogger('uvicorn.error')

router = APIRouter()



@router.get("", response_model=List[PatientSchema])  # Added response_model
async def get_all_patients(db: Session = Depends(get_db)):
    patients = db.query(Patient).all()

    return patients


@router.post("", response_model=PatientSchema)
async def create_patient(patient: CreatePatientSchema, db: Session = Depends(get_db)):
    # check if patient exists
    db_patient = db.query(Patient).filter(Patient.name == patient.name).first()
    if db_patient is not None:
        raise HTTPException(status_code=400, detail="Patient already exists")
    db_patient = Patient(
        name=patient.name,
        telecom=patient.telecom,
        address=patient.address,
        email=patient.email,
        medecin_id=patient.medecin_id
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
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
    db.commit()
    db.refresh(db_patient)
    return db_patient


@router.delete("")
def delete_patient(patient_id: Dict[str, int], db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.id == patient_id['id']).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted successfully"}
