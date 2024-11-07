from typing import Optional

from pydantic import BaseModel


class CabinetMedicalSchema(BaseModel):
    id: int
    active: Optional[bool] = True
    name: str
    telecom: Optional[str] = None
    address: Optional[str] = None
    type: Optional[str] = None
