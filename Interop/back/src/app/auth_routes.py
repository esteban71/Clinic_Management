from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import Patient
from src.schemas import PatientSchema
from src.utils.auth import get_access_token
from keycloak import KeycloakOpenID
import logging
from fastapi import FastAPI, HTTPException, status, Header
from keycloak import KeycloakOpenID
import httpx
import logging
from pydantic import BaseModel
import asyncio
from typing import Optional, Dict, Any
from fastapi.responses import JSONResponse
import jwt

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('uvicorn.error')


# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int


KEYCLOAK_CONFIG = {
    "server_url": "http://keycloak:8080/",
    "client_id": "backend",
    "realm_name": "master",
    "client_secret_key": "kjhk0CE0jOirTWyM89TJadN8wwFd1xkD"
}


@router.post("/login", response_model=LoginResponse)
async def login_with_keycloak(form_data: LoginRequest) -> Dict[str, Any]:
    try:
        keycloak_openid = KeycloakOpenID(
            server_url=KEYCLOAK_CONFIG["server_url"],
            client_id=KEYCLOAK_CONFIG["client_id"],
            realm_name=KEYCLOAK_CONFIG["realm_name"],
            client_secret_key=KEYCLOAK_CONFIG["client_secret_key"],
            timeout=10000
        )

        # Authenticate and get tokens from Keycloak
        token = keycloak_openid.token(form_data.username, form_data.password)
        logger.info(f"Login successful for user {form_data.username}")

        # Create response with access token and user info
        response_data = {
            "accessToken": token["access_token"]
        }

        # Set refresh token as a secure cookie
        response = JSONResponse(status_code=200, content=response_data)
        response.set_cookie(
            key="jwt",
            value=token["refresh_token"],
            httponly=True,
            secure=True,
            samesite="None",
            max_age=7 * 24 * 60 * 60 * 1000  # 7 days in milliseconds
        )

        return response

    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )


@router.get("/refresh", response_model=LoginResponse)
async def refresh_token(
        jwt: Annotated[str | None, Cookie()] = None
) -> Dict[str, Any]:
    refresh_token = jwt
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token not provided"
        )

    try:
        # Initialize Keycloak client
        keycloak_openid = KeycloakOpenID(
            server_url=KEYCLOAK_CONFIG["server_url"],
            client_id=KEYCLOAK_CONFIG["client_id"],
            realm_name=KEYCLOAK_CONFIG["realm_name"],
            client_secret_key=KEYCLOAK_CONFIG["client_secret_key"],
            timeout=10000
        )

        # Use Keycloak to refresh the token
        token = keycloak_openid.refresh_token(refresh_token)
        logger.info("Token successfully refreshed.")

        # Prepare response data
        response_data = {
            "accessToken": token["access_token"]
        }

        # Set the new refresh token as a secure HTTP-only cookie
        response = JSONResponse(status_code=200, content=response_data)
        response.set_cookie(
            key="jwt",
            value=token["refresh_token"],
            httponly=True,
            secure=True,
            samesite="None",
            max_age=7 * 24 * 60 * 60 * 1000  # 7 days
        )

        return response

    except Exception as e:
        logger.error(f"Token refresh failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token refresh failed"
        )


@router.post("/logout")
async def logout() -> JSONResponse:
    response = JSONResponse(status_code=200, content={"message": "Cookie cleared"})
    response.delete_cookie("jwt", httponly=True, samesite="None", secure=True)
    return response
