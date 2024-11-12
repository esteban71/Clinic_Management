import logging
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import Patient, Medecin, DossierMedical
from src.schemas import PatientSchema
from src.schemas.PatientSchema import CreatePatientSchema

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
        id=db.query(Patient).count(),
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
        id=db.query(DossierMedical).count(),
        patient_id=db_patient.id,
    )
    db.add(db_dossier_medical)
    db.commit()
    db.refresh(db_patient)
    db.refresh(db_dossier_medical)
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
    return db_patient


@router.delete("")
def delete_patient(patient_id: Dict[str, int], db: Session = Depends(get_db)):
    db_patient = db.query(Patient).filter(Patient.id == patient_id['id']).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted successfully"}
