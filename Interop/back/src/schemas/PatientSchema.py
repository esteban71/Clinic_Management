from pydantic import BaseModel
from datetime import date


from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List, Dict


class CommunicationSchema(BaseModel):
    id: int
    language: Optional[str] = None
    preferred: Optional[bool] = None

    class Config:
        orm_mode = True


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
    deceased: Optional[Dict[str, Optional[str]]] = None  # {"deceased": bool, "date": date}
    address: Optional[str] = None
    marital_status: Optional[str] = None
    multiple_birth: Optional[bool] = None
    photo: Optional[str] = None
    general_practitioner: Optional[str] = None
    managing_organization: Optional[str] = None

    links: List[LinkSchema] = []
    contacts: List[ContactSchema] = []
    communications: List[CommunicationSchema] = []

    class Config:
        orm_mode = True
