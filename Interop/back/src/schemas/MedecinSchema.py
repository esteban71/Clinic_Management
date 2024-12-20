from typing import Optional

from pydantic import BaseModel


class MedecinSchema(BaseModel):
    id: int
    rpps: Optional[str] = None
    name: str
    specialite: Optional[str] = None
    email: Optional[str] = None
    telecom: Optional[str] = None
    habilitations: Optional[str] = None
    cabinet_medical_id: Optional[int] = None
    username: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True


class CreateMedecinSchema(BaseModel):
    name: str
    telecom: str
    username: str
    email: str
    password: str
    cabinet_id: int


class UpdateMedecinSchema(BaseModel):
    id: int
    name: str
    telecom: str
    newusername: str
    username: str
    cabinet_id: int
    email: str
    password: Optional[str] = None
