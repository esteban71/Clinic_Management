import logging
from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import Secretariat
from src.schemas.SecretariatSchema import SecretariatSchema, CreateSecretariatSchema, UpdateSecretariatSchema
from src.utils.auth import create_user, add_attribute_to_user, modify_user, delete_user

logger = logging.getLogger('uvicorn.error')

router = APIRouter()


@router.get("", response_model=List[SecretariatSchema])
async def get_all_secretariat(request: Request, db: Session = Depends(get_db)):
    secretariat = db.query(Secretariat).all()
    return secretariat


@router.post("")
async def create_Secretariat(secretariat: CreateSecretariatSchema, db: Session = Depends(get_db)):
    db_secretariat = db.query(Secretariat).filter(Secretariat.username == secretariat.username).first()
    if db_secretariat is not None:
        raise HTTPException(status_code=400, detail="Secretariat already exists")
    result = await create_user(
        username=secretariat.username,
        email=secretariat.email,
        password=secretariat.password,
        role="Receptionist",
    )
    if result:
        db_secretariat = Secretariat(
            name=secretariat.name,
            telecom=secretariat.telecom,
            email=secretariat.email,
            username=secretariat.username,
            cabinet_medical_id=secretariat.cabinet_id
        )
        db.add(db_secretariat)
        db.commit()
        db.refresh(db_secretariat)
        await add_attribute_to_user(secretariat.username,
                                    {"cabinet_id": secretariat.cabinet_id, "Secretariat_id": db_secretariat.id})
        return db_secretariat
    else:
        logger.error(f"Error creating medecin: {secretariat.username}")
        raise HTTPException(status_code=400, detail="Error creating medecin")


@router.patch("")
async def update_scretariat(secretariat: UpdateSecretariatSchema, db: Session = Depends(get_db)):
    db_secretariat = db.query(Secretariat).filter(Secretariat.id == secretariat.id).first()
    if db_secretariat is None:
        raise HTTPException(status_code=404, detail="secretariat not found")
    await modify_user(
        newusername=secretariat.newusername,
        username=secretariat.username,
        email=secretariat.email,
        cabinet_id=secretariat.cabinet_id,
        password=secretariat.password)

    db_secretariat.name = secretariat.name
    db_secretariat.username = secretariat.newusername
    db_secretariat.telecom = secretariat.telecom
    db_secretariat.email = secretariat.email
    db_secretariat.cabinet_medical_id = secretariat.cabinet_id

    db.commit()
    db.refresh(db_secretariat)
    return db_secretariat


@router.delete("")
async def delete_secretariat(secretariat_id: Dict[str, int], db: Session = Depends(get_db)):
    db_secretariat = db.query(Secretariat).filter(Secretariat.id == secretariat_id['id']).first()
    if db_secretariat is None:
        raise HTTPException(status_code=404, detail="Secretariat not found")
    db.delete(db_secretariat)
    db.commit()
    await delete_user(db_secretariat.username)
    return db_secretariat
