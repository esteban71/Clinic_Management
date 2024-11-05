import logging
from typing import List

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
    logger.info(f"Request: {request.state.user}")
    medecins = db.query(Medecin).all()

    return medecins


class CreateMedecinSchema(BaseModel):
    name: str
    telecom: str
    username: str
    email: str
    password: str


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
        )
        db.add(db_medecin)
        db.commit()
        db.refresh(db_medecin)
        await add_attribute_to_user(medecin.username, {"medecin_id": db_medecin.id})
        return db_medecin
    else:
        logger.error(f"Error creating medecin: {medecin.username}")
        raise HTTPException(status_code=400, detail="Error creating medecin")
