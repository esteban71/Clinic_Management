from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.model import Patient
from src.schemas import MedecinSchema
from src.model import Medecin
from typing import Dict, Any, List

router = APIRouter()


@router.get("", response_model=List[MedecinSchema])
async def get_all_medecins(db: Session = Depends(get_db)):
    medecins = db.query(Medecin).all()

    return medecins

