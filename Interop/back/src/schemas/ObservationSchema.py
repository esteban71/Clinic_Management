from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from src.schemas.DispositifMedicauxSchema import DispositifMedicauxSchema
from src.schemas.PatientSchema import PatientSchema


class CreateObservationSchema(BaseModel):
    date_time: Optional[datetime] = None
    code: Optional[str] = None
    value: Optional[str] = None
    unit: Optional[str] = None
    status: str = None

    component_code: Optional[str] = None
    component_value: Optional[str] = None
    component_unit: Optional[str] = None

    patient_id: int = None
    device_id: int = None

    class Config:
        orm_mode = True
        from_attributes = True


class ObservationSchema(BaseModel):
    id: int
    date_time: Optional[datetime] = None
    code: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    status: str = None

    component_code: Optional[str] = None
    component_value: Optional[float] = None
    component_unit: Optional[str] = None

    patient_id: int = None
    device_id: int = None

    patient: Optional[PatientSchema] = None
    device: Optional[DispositifMedicauxSchema] = None

    class Config:
        orm_mode = True
        from_attributes = True
