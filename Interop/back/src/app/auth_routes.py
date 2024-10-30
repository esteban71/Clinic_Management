from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import Patient
from src.schemas import PatientSchema
from src.utils.auth import get_access_token
from keycloak import KeycloakOpenID
import logging
router = APIRouter()

logger = logging.getLogger('uvicorn.error')
from pydantic import BaseModel


keycloak_openid = KeycloakOpenID(server_url="http://localhost:8081/",
                                 client_id="backend",
                                 realm_name="master",
                                 client_secret_key="kjhk0CE0jOirTWyM89TJadN8wwFd1xkD")


class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login_with_keycloak(form_data: LoginRequest):
    try:
        token = await keycloak_openid.a_token(form_data.username, form_data.password)
        logger.info(f"Token: {token}")
        return token
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"error": str(e)}



@router.get("/refresh")
async def refresh():
    return {"message": "Refresh page"}
