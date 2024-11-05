import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Header, Body, Cookie, Request
from keycloak import KeycloakAdmin, KeycloakOpenIDConnection, KeycloakOpenID
from src.schemas.AuthSchema import LoginRequest

logger = logging.getLogger('uvicorn.error')

KEYCLOAK_CONFIG = {
    "server_url": "http://keycloak:8080/",
    "client_id": "backend",
    "realm_name": "master",
    "client_secret_key": "**********",
    "username": "admin",
    "password": "password"
}


def get_keycloak_openid_connection():
    return KeycloakOpenIDConnection(
        server_url=KEYCLOAK_CONFIG["server_url"],
        username=KEYCLOAK_CONFIG["username"],
        password=KEYCLOAK_CONFIG["password"],
        client_id=KEYCLOAK_CONFIG["client_id"],
        realm_name=KEYCLOAK_CONFIG["realm_name"],
        client_secret_key=KEYCLOAK_CONFIG["client_secret_key"],
        verify=True
    )


def get_keycloak_admin_connection(
        connection: KeycloakOpenIDConnection = get_keycloak_openid_connection):
    return KeycloakAdmin(connection=connection())


async def get_keycloak_openid():
    return KeycloakOpenID(
        server_url=KEYCLOAK_CONFIG["server_url"],
        client_id=KEYCLOAK_CONFIG["client_id"],
        realm_name=KEYCLOAK_CONFIG["realm_name"],
        client_secret_key=KEYCLOAK_CONFIG["client_secret_key"],
        timeout=10000
    )


async def get_user_token(keycloak_openid: KeycloakOpenID = Depends(get_keycloak_openid),
                         form_data: LoginRequest = Body()):
    try:
        token = keycloak_openid.token(form_data.username, form_data.password)
        return token
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials")


async def get_user_token_with_refresh(keycloak_openid: KeycloakOpenID = Depends(get_keycloak_openid),
                                      jwt: Annotated[str | None, Cookie()] = None):
    try:
        token = keycloak_openid.refresh_token(jwt)
        return token
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials")


async def logout_user(keycloak_openid: KeycloakOpenID = Depends(get_keycloak_openid),
                      jwt: Annotated[str | None, Cookie()] = None):
    try:
        keycloak_openid.logout(jwt)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Error logging out")


async def create_user(username: str, email: str, password: str, role: str,
                      connection_admin: KeycloakAdmin = get_keycloak_admin_connection):
    result = connection_admin().create_user({
        "username": username,
        "email": email,
        "enabled": True,
        "credentials": [{"type": "password", "value": password}]
    })
    user_id = connection_admin().get_user_id(username)
    role = connection_admin().get_realm_role(role)
    if role and user_id:
        connection_admin().assign_realm_roles(user_id=user_id, roles=[role])
    else:
        raise HTTPException(status_code=400, detail="Error creating account")

    return result


async def add_attribute_to_user(username: str, attribute: dict,
                                connection_admin: KeycloakAdmin = get_keycloak_admin_connection):
    try:
        user_id = connection_admin().get_user_id(username)
        connection_admin().update_user(user_id, payload={"attributes": attribute})
    except Exception as e:
        logger.info(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Error updating account")


async def delete_user(username: str, connection_admin: KeycloakAdmin = get_keycloak_admin_connection):
    user_id = connection_admin().get_user_id(username)
    result = connection_admin().delete_user(user_id)
    if not result:
        raise HTTPException(status_code=400, detail="Error deleting account")


def protected_route(required_roles: list):
    async def wrapper(request: Request, authorization: Annotated[str, Header()]):
        try:
            token = authorization.split("Bearer ")[-1] if authorization.startswith("Bearer ") else authorization
            keycloak_openid = await get_keycloak_openid()
            valid = keycloak_openid.introspect(token)
            if not valid.get("active", False):
                raise HTTPException(status_code=401, detail="Unauthorized")

            roles = valid.get("realm_access", {}).get("roles", [])
            if not any(role in required_roles for role in roles):
                raise HTTPException(status_code=401, detail="Forbidden: Insufficient permissions")
            request.state.user = keycloak_openid.decode_token(token)
            return {"token": token, "user": valid}
        except Exception as e:
            logger.info(f"Error: {e}")
            raise HTTPException(status_code=401, detail="Unauthorized")

    return wrapper
