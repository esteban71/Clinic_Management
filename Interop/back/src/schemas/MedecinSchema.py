from pydantic import BaseModel
from datetime import date,datetime


from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List, Dict



class MedecinSchema(BaseModel):
    id: int
    rpps: Optional[str] = None
    name: str
    specialite: Optional[str] = None
    email: Optional[str] = None
    telecom: Optional[str] = None
    habilitations: Optional[str] = None
    cabinet_medical_id: Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True