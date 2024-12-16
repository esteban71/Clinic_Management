import logging
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.database import get_db
from src.model.DispositifMedicaux import DispositifMedicaux
from src.model.Observation import Observation
from src.schemas.ObservationSchema import CreateObservationSchema, ObservationSchema

logger = logging.getLogger('uvicorn.error')

router = APIRouter()


@router.get("/{patient_id}/observations", response_model=List[ObservationSchema])
async def get_observations(patient_id: int, db: Session = Depends(get_db)):
    dispositif_medical = db.query(DispositifMedicaux).filter(DispositifMedicaux.patient_id == patient_id).first()
    if not dispositif_medical:
        raise HTTPException(status_code=404, detail="dispositif médical not found")
    observations = db.query(Observation).filter(Observation.device_id == dispositif_medical.id).all()
    if not observations:
        return []
    return observations


@router.post("/{patient_id}/observations/new", response_model=CreateObservationSchema)
async def create_observations(request: Request, patient_id: int, report: CreateObservationSchema,
                              db: Session = Depends(get_db)):
    dispositif_medical = db.query(DispositifMedicaux).filter(DispositifMedicaux.patient_id == patient_id).first()

    if not dispositif_medical:
        raise HTTPException(status_code=404, detail="Medical device not found")

    new_observation = Observation(
        date_time=datetime.now(),
        code=report.title,
        value=report.content,
        unit=report.unit,
        status="final",
        patient_id=patient_id,
        device_id=dispositif_medical.id,
        component_code=report.component_code,
        component_value=report.component_value,
        component_unit=report.component_unit
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report


# Route pour supprimer un rapport médical d'un patient
@router.delete("/{patient_id}/observations/{report_id}")
async def delete_observations(patient_id: int, report_id: int, db: Session = Depends(get_db)):
    observation = db.query(Observation).filter(Observation.id == report_id).first()

    if not observation:
        raise HTTPException(status_code=404, detail="Medical report not found")

    db.delete(observation)
    db.commit()
    return {"message": "Medical report deleted successfully"}


