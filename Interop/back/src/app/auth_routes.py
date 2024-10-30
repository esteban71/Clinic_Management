from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import Patient
from src.schemas import PatientSchema
import httpx
from src.utils.auth import get_access_token

router = APIRouter()

KEYCLOAK_URL = "http://localhost:8081/to/realm/protocol/openid-connect/token"
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"

from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login_with_keycloak(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await get_access_token(form_data)



@router.get("/refresh")
async def refresh():
    return {"message": "Refresh page"}
