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