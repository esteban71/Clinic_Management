from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from src.schemas.PatientSchema import PatientSchema


class DispositifMedicauxSchema(BaseModel):
    id: int
    name: Optional[str] = None
    type: Optional[str] = None
    interval: Optional[int] = None
    status: Optional[str] = None
    manufacturer: Optional[str] = None
    serial_number: Optional[str] = None
    lot_number: Optional[str] = None
    manufacture_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None
    patient_id: int = None
    patient: Optional[PatientSchema] = None

    class Config:
        orm_mode = True
        from_attributes = True
