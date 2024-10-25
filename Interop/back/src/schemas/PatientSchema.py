from pydantic import BaseModel
from datetime import date


class PatientSchema(BaseModel):
    id: int
    name: str
    birthdate: date
    sexe: str

    class Config:
        from_attributes = True