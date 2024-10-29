from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from src.model.Base import Base
from src.model.Patient import Patient

class DossierMedical(Base):
    __tablename__ = 'dossiers_medicaux'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    date_creation = Column(Date, nullable=True)
    type_acces = Column(String, nullable=True)

    patient = relationship("Patient", back_populates="dossiers_medicaux")

class DossierAdministratif(Base):
    __tablename__ = 'dossiers_administratifs'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    date_creation = Column(Date, nullable=True)
    documents = Column(JSON, nullable=True)

    patient = relationship("Patient", back_populates="dossiers_administratifs")

class CompteRenduMedical(Base):
    __tablename__ = 'comptes_rendus_medicaux'
    
    id = Column(Integer, primary_key=True)
    dossier_medical_id = Column(Integer, ForeignKey('dossiers_medicaux.id'))
    date = Column(Date, nullable=True)
    type = Column(String, nullable=True)
    contenu = Column(String, nullable=True)

    cabinet_medical = relationship("DossierMedical", back_populates="comptes_rendus_medicaux")