from typing import Annotated

import jwt
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from jwt import PyJWKClient

from .database import SessionLocal
from .models import Patient as Patient
from .schemas import PatientSchema as PatientSchema

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth_2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl="http://localhost:8080/to/realm/protocol/openid-connect/token",
    authorizationUrl="http://localhost:8080/to/realm/protocol/openid-connect/auth",
    refreshUrl="http://localhost:8080/to/realm/protocol/openid-connect/token",
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


def has_role(role_name: str):
    async def check_role(
            token_data: Annotated[dict, Depends(valid_access_token)]
    ):
        roles = token_data["resource_access"]["api"]["roles"]
        if role_name not in roles:
            raise HTTPException(status_code=403, detail="Unauthorized access")

    return check_role


@app.get("/public")
def get_public():
    return {"message": "This endpoint is public"}


@app.get("/private", dependencies=[Depends(valid_access_token)])
def get_private():
    return {"message": "This endpoint is private"}

@app.get("/patients/{patient_id}", response_model=PatientSchema)
def get_patient(patient_id: int, db=Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

