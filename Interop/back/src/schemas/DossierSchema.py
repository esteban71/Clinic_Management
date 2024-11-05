from pydantic import BaseModel
from datetime import date
from typing import Optional, List, Dict

class CompteRenduMedicalSchema(BaseModel):
    id: int
    dossier_medical_id: Optional[int] = None
    date: Optional[date] = None
    type: Optional[str] = None
    contenu: Optional[str] = None
    auteur_id: Optional[int] = None  # ID du médecin qui a rédigé le compte-rendu

    class Config:
        orm_mode = True
        from_attributes = True


class DossierMedicalSchema(BaseModel):
    id: int
    patient_id: Optional[int] = None
    date_creation: Optional[date] = None
    type_acces: Optional[str] = None
    cabinet_medical_id: Optional[int] = None
    comptes_rendus: List[CompteRenduMedicalSchema] = []  # Liste des comptes rendus médicaux associés

    class Config:
        orm_mode = True
        from_attributes = True


class DossierAdministratifSchema(BaseModel):
    id: int
    patient_id: Optional[int] = None
    date_creation: Optional[date] = None
    documents: Optional[dict] = None  # JSON des documents administratifs

    class Config:
        orm_mode = True
        from_attributes = True
