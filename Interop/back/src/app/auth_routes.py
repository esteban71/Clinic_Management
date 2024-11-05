from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, Request, Body
from fastapi import HTTPException, status
from keycloak import KeycloakOpenID
import logging
from typing import Dict, Any
from fastapi.responses import JSONResponse

from src.schemas.AuthSchema import LoginRequest, LoginResponse
from src.utils.auth import get_user_token, get_user_token_with_refresh, logout_user

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('uvicorn.error')


@router.post("/login", response_model=LoginResponse)
async def login_with_keycloak(token: Dict[str, Any] = Depends(get_user_token)) -> JSONResponse:
    try:
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
        token: Dict[str, Any] = Depends(get_user_token_with_refresh),
) -> Dict[str, Any]:
    try:
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
async def logout(logout_user: None = Depends(logout_user)) -> JSONResponse:
    response = JSONResponse(status_code=200, content={"message": "Cookie cleared"})
    response.delete_cookie("jwt", httponly=True, samesite="None", secure=True)
    return response
