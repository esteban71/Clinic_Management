from pydantic import BaseModel


class PatientSchema(BaseModel):
    id: int
    name: str
    birthdate: str
    sexe: str