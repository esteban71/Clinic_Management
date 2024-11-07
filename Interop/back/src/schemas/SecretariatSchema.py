from typing import Optional

from pydantic import BaseModel

from .CabinetMedicalSchema import CabinetMedicalSchema


class SecretariatSchema(BaseModel):
    id: int
    name: str
    username: Optional[str] = None
    email: Optional[str] = None
    telecom: Optional[str] = None
    cabinet_medical_id: int = None
    cabinet_medical: CabinetMedicalSchema = None

    class Config:
        orm_mode = True
        from_attributes = True


class CreateSecretariatSchema(BaseModel):
    name: str
    telecom: str
    username: str
    email: str
    password: str
    cabinet_id: int


class UpdateSecretariatSchema(BaseModel):
    id: int
    name: str
    telecom: str
    newusername: str
    username: str
    cabinet_id: int
    email: str
    password: Optional[str] = None
