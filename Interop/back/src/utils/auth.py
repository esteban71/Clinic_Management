from typing import Annotated
from fastapi import Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer
import jwt
from jwt import PyJWKClient
import os
import httpx
import logging
import sys

logger = logging.getLogger('uvicorn.error')

oauth_2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="http://localhost:8081/to/master/protocol/openid-connect/token",
    authorizationUrl="http://localhost:8081/to/realm/protocol/openid-connect/auth",
    refreshUrl="http://localhost:8081/to/realm/protocol/openid-connect/token",
)

CLIENT_ID, CLIENT_SECRET, KEYCLOAK_URL = os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"), os.getenv("KEYCLOAK_URL")


async def get_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    logger.info(f"Getting access token for {form_data.username}")
    logger.info(f"CLIENT_ID: {CLIENT_ID}")
    logger.info(f"CLIENT_SECRET: {CLIENT_SECRET}")
    logger.info(f"KEYCLOAK_URL: {KEYCLOAK_URL}")
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "password",
        "username": form_data.username,
        "password": form_data.password,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(KEYCLOAK_URL, data=payload)

    if response.status_code == 200:
        token_data = response.json()
        return {
            "access_token": token_data["access_token"],
            "refresh_token": token_data["refresh_token"],
            "token_type": "bearer",
            "expires_in": token_data["expires_in"],
        }
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Invalid credentials or Keycloak configuration",
        )


async def valid_access_token(
        access_token: Annotated[str, Depends(oauth_2_scheme)]
):
    url = "http://localhost:8080/to/realm/protocol/openid-connect/certs"
    optional_custom_headers = {"User-agent": "custom-user-agent"}
    jwks_client = PyJWKClient(url, headers=optional_custom_headers)

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        data = jwt.decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            audience="api",
            options={"verify_exp": True},
        )
        return data
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Not authenticated")


def check_role(authorization: Annotated[str | None, Header()] = None):
    def check_role_decorator(func):
        async def wrapper(
                token_data: Annotated[dict, Depends(valid_access_token)]
        ):
            roles = token_data["resource_access"]["api"]["roles"]
            if authorization not in roles:
                raise HTTPException(status_code=403, detail="Unauthorized access")

            return await func(token_data)

        return wrapper
