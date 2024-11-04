from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import Patient
from src.schemas import MedecinSchema
from src.model import Medecin
from typing import Dict, Any, List
from pydantic import BaseModel
from keycloak import KeycloakAdmin
from keycloak import KeycloakOpenIDConnection
import logging

logger = logging.getLogger('uvicorn.error')

router = APIRouter()

KEYCLOAK_CONFIG = {
    "server_url": "http://keycloak:8080/",
    "client_id": "backend",
    "realm_name": "master",
    "client_secret_key": "kjhk0CE0jOirTWyM89TJadN8wwFd1xkD",
    "username": "admin",
    "password": "password"
}


@router.get("", response_model=List[MedecinSchema])
async def get_all_medecins(db: Session = Depends(get_db)):
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

    keycloak_connection = KeycloakOpenIDConnection(
        server_url=KEYCLOAK_CONFIG["server_url"],
        username=KEYCLOAK_CONFIG["username"],
        password=KEYCLOAK_CONFIG["password"],
        client_id=KEYCLOAK_CONFIG["client_id"],
        realm_name=KEYCLOAK_CONFIG["realm_name"],
        client_secret_key=KEYCLOAK_CONFIG["client_secret_key"],
        verify=True
    )
    keycloak_admin = KeycloakAdmin(connection=keycloak_connection)
    result = keycloak_admin.create_user({
        "username": medecin.username,
        "email": medecin.email,
        "enabled": True,
        "credentials": [{"type": "password", "value": medecin.password}]
    })

    user_id = keycloak_admin.get_user_id(medecin.username)

    role = keycloak_admin.get_realm_role("Doctor")

    if role and user_id:
        keycloak_admin.assign_realm_roles(user_id=user_id, roles=[role])
    if result:
        db_medecin = Medecin(
            name=medecin.name,
            telecom=medecin.telecom,
            email=medecin.email,
        )
        db.add(db_medecin)
        db.commit()
        db.refresh(db_medecin)
        keycloak_admin.update_user(user_id, {
            "attributes": {
                "medecin_id": str(db_medecin.id)
            }
        })
        return db_medecin
    else:
        raise HTTPException(status_code=400, detail="Error creating medecin")
