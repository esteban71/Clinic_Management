from pydantic import BaseModel
from datetime import date


from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List, Dict
from src.schemas.MedecinSchema import MedecinSchema


class ContactSchema(BaseModel):
    id: int
    relationship: Optional[str] = None
    role: Optional[str] = None
    name: Optional[str] = None
    additional_name: Optional[str] = None
    telecom: Optional[str] = None
    address: Optional[str] = None
    additional_address: Optional[str] = None
    gender: Optional[str] = None
    organization: Optional[str] = None
    period: Optional[str] = None

    class Config:
        orm_mode = True


class LinkSchema(BaseModel):
    id: int
    type: Optional[str] = None
    other: Optional[int] = None  # Link to another patient's id

    class Config:
        orm_mode = True


class PatientSchema(BaseModel):
    id: int
    active: Optional[bool] = None
    name: str
    telecom: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    address: Optional[str] = None
    marital_status: Optional[str] = None
    managing_organization: Optional[str] = None

    links: List[LinkSchema] = []
    contacts: List[ContactSchema] = []
    medecin: Optional[MedecinSchema] = None

    class Config:
        orm_mode = True
