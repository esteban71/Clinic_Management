import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import Medecin
from src.schemas import MedecinSchema
from src.utils.auth import create_user, add_attribute_to_user

logger = logging.getLogger('uvicorn.error')

router = APIRouter()


@router.get("", response_model=List[MedecinSchema])
async def get_all_medecins(request: Request, db: Session = Depends(get_db)):
    medecins = db.query(Medecin).all()
    return medecins


class CreateMedecinSchema(BaseModel):
    name: str
    telecom: str
    username: str
    email: str
    password: str
    cabinet_id: int


class UpdateMedecinSchema(BaseModel):
    name: str
    telecom: str
    email: str
    username: str
    password: Optional[str] = None


@router.post("")
async def create_medecin(medecin: CreateMedecinSchema, db: Session = Depends(get_db)):

    db_medecin = db.query(Medecin).filter(Medecin.name == medecin.name).first()
    if db_medecin is not None:
        raise HTTPException(status_code=400, detail="Medecin already exists")
    result = await create_user(
        username=medecin.username,
        email=medecin.email,
        password=medecin.password,
        role="Doctor",
    )
    if result:
        db_medecin = Medecin(
            name=medecin.name,
            telecom=medecin.telecom,
            email=medecin.email,
            username=medecin.username,
            cabinet_medical_id=medecin.cabinet_id
        )
        db.add(db_medecin)
        db.commit()
        db.refresh(db_medecin)
        await add_attribute_to_user(medecin.username, {"cabinet_id": medecin.cabinet_id, "medecin_id": db_medecin.id})
        return db_medecin
    else:
        logger.error(f"Error creating medecin: {medecin.username}")
        raise HTTPException(status_code=400, detail="Error creating medecin")


@router.patch("")
def update_medecin(medecin: UpdateMedecinSchema, db: Session = Depends(get_db)):
    db_medecin = db.query(Medecin).filter(Medecin.username == medecin.username).first()
    if db_medecin is None:
        raise HTTPException(status_code=404, detail="Medecin not found")

    db_medecin.name = medecin.name
    db_medecin.telecom = medecin.telecom
    db_medecin.email = medecin.email
    db.commit()
    db.refresh(db_medecin)
    return db_medecin
