import logging
from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import Medecin
from src.schemas import MedecinSchema, CreateMedecinSchema, UpdateMedecinSchema
from src.utils.auth import create_user, add_attribute_to_user, modify_user, delete_user

logger = logging.getLogger('uvicorn.error')

router = APIRouter()


@router.get("", response_model=List[MedecinSchema])
async def get_all_medecins(request: Request, db: Session = Depends(get_db)):
    if request.state.user["attributes"].get("cabinet_id") is not None:
        cabinet_id = int(request.state.user["attributes"]["cabinet_id"][0])
        logger.info(f"Getting medecin with id {cabinet_id}")
        medecins = db.query(Medecin).filter(Medecin.cabinet_medical_id == cabinet_id).all()
        if medecins is None:
            raise HTTPException(status_code=404, detail="Medecin not found")
        return medecins
    medecins = db.query(Medecin).all()
    return medecins


@router.post("")
async def create_medecin(medecin: CreateMedecinSchema, db: Session = Depends(get_db)):
    db_medecin = db.query(Medecin).filter(Medecin.username == medecin.username).first()
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
            cabinet_medical_id=medecin.cabinet_id,
            specialite="cardiologist"
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
async def update_medecin(medecin: UpdateMedecinSchema, db: Session = Depends(get_db)):
    db_medecin = db.query(Medecin).filter(Medecin.id == medecin.id).first()
    if db_medecin is None:
        raise HTTPException(status_code=404, detail="Medecin not found")
    await modify_user(
        newusername=medecin.newusername,
        username=medecin.username,
        email=medecin.email,
        cabinet_id=medecin.cabinet_id,
        password=medecin.password)

    db_medecin.name = medecin.name
    db_medecin.username = medecin.newusername
    db_medecin.telecom = medecin.telecom
    db_medecin.email = medecin.email
    db_medecin.cabinet_medical_id = medecin.cabinet_id

    db.commit()
    db.refresh(db_medecin)
    return db_medecin


@router.delete("")
async def delete_medecin(medecin_id: Dict[str, int], db: Session = Depends(get_db)):
    db_medecin = db.query(Medecin).filter(Medecin.id == medecin_id['id']).first()
    if db_medecin is None:
        raise HTTPException(status_code=404, detail="Medecin not found")
    db.delete(db_medecin)
    db.commit()
    await delete_user(db_medecin.username)
    return db_medecin
