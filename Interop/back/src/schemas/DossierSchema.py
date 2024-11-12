from datetime import date
from typing import Optional, List

from pydantic import BaseModel

class CreateCompteRenduMedicalSchema(BaseModel):
    title: str
    content: str
    date: str  # Utiliser une chaîne pour éviter les erreurs de validation lors de l'envoi depuis le frontend
    patient_id: int

    class Config:
        orm_mode = True
        from_attributes = True

class CompteRenduMedicalSchema(BaseModel):
    id: int
    dossier_medical_id: Optional[int] = None
    title: str
    content: str
    date: date
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


class CreateDossierMedicalSchema(BaseModel):
    patient_id: Optional[int] = None
    type_acces: Optional[str] = None
    cabinet_medical_id: Optional[int] = None

    class Config:
        orm_mode = True
        from_attributes = True
