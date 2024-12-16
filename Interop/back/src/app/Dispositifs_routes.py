import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.database import get_db
from src.model.DispositifMedicaux import DispositifMedicaux
from src.schemas.DispositifMedicauxSchema import DispositifMedicauxSchema, CreateDispositifMedicauxSchema

logger = logging.getLogger('uvicorn.error')

router = APIRouter()


# Route pour obtenir tous les dossiers médicaux d'un patient
@router.get("/{patient_id}/dispositifs", response_model=List[DispositifMedicauxSchema])
async def get_dispositifs(patient_id: int, db: Session = Depends(get_db)):
    dispositifs = db.query(DispositifMedicaux).filter(DispositifMedicaux.patient_id == patient_id).all()
    return dispositifs


@router.post("/{patient_id}/new", response_model=DispositifMedicauxSchema)
async def create_dispositif(request: Request, patient_id: int, report: CreateDispositifMedicauxSchema,
                            db: Session = Depends(get_db)):
    new_dispositif = DispositifMedicaux(
        patient_id=patient_id,
        name=report.name,
        type=report.type,
        status=report.status,
        manufacturer=report.manufacturer,
        serial_number=report.serial_number,
        lot_number=report.lot_number,
        manufacture_date=report.manufacture_date,
        expiration_date=report.expiration_date,
    )

    db.add(new_dispositif)
    db.commit()
    db.refresh(new_dispositif)
    return new_dispositif


@router.patch("/{patient_id}/dispositif/{dispositif_id}", response_model=DispositifMedicauxSchema)
async def update_dispositifs(patient_id: int, dispositif_id: int, report: CreateDispositifMedicauxSchema,
                             db: Session = Depends(get_db)):
    dispositif = db.query(DispositifMedicaux).filter(
        DispositifMedicaux.id == dispositif_id
    ).first()

    if not dispositif:
        raise HTTPException(status_code=404, detail="Medical device not found")

    dispositif.name = report.name
    dispositif.type = report.type
    dispositif.interval = report.interval
    dispositif.status = report.status
    dispositif.manufacturer = report.manufacturer
    dispositif.serial_number = report.serial_number
    dispositif.lot_number = report.lot_number
    dispositif.manufacture_date = report.manufacture_date
    dispositif.expiration_date = report.expiration_date
    db.commit()
    db.refresh(dispositif)
    return dispositif


# Route pour supprimer un rapport médical d'un patient
@router.delete("/{patient_id}/dispositif/{dispositif_id}")
async def delete_dispositifs(patient_id: int, dispositif_id: int, db: Session = Depends(get_db)):
    dispositif = db.query(DispositifMedicaux).filter(
        DispositifMedicaux.id == dispositif_id,
    ).first()

    if not dispositif:
        raise HTTPException(status_code=404, detail="Medical device not found")

    db.delete(dispositif)
    db.commit()
    return {"message": "Medical device deleted successfully"}
