import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import CabinetMedical
from src.schemas import CabinetMedicalSchema

logger = logging.getLogger('uvicorn.error')

router = APIRouter()


@router.get("", response_model=List[CabinetMedicalSchema])
async def get_all_cabinets(request: Request, db: Session = Depends(get_db)):
    if request.state.user["attributes"].get("cabinet_id") is not None:
        cabinet_id = int(request.state.user["attributes"]["cabinet_id"][0])
        logger.info(f"Getting cabinet with id {cabinet_id}")
        cabinet = db.query(CabinetMedical).filter(CabinetMedical.id == cabinet_id).first()
        if cabinet is None:
            raise HTTPException(status_code=404, detail="Cabinet not found")
        return [cabinet]
    roles = valid.get("realm_access", {}).get("roles", [])
    if "admin" in roles:
        cabinets = db.query(CabinetMedical).all()
        return cabinets
    else:
        raise HTTPException(status_code=403, detail="Unauthorized")
