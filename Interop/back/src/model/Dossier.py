from sqlalchemy import Column, Integer, String, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from src.model.Base import Base


class DossierMedical(Base):
    __tablename__ = 'dossiers_medicaux'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    date_creation = Column(Date, nullable=True)
    type_acces = Column(String, nullable=True)

    patient = relationship("Patient", back_populates="dossier_medical")
    comptes_rendus = relationship("CompteRenduMedical", back_populates="dossier_medical")


class DossierAdministratif(Base):
    __tablename__ = 'dossiers_administratifs'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    date_creation = Column(Date, nullable=True)
    documents = Column(JSON, nullable=True)

    patient = relationship("Patient", back_populates="dossier_administratif")


class CompteRenduMedical(Base):
    __tablename__ = 'comptes_rendus_medicaux'

    id = Column(Integer, primary_key=True)
    dossier_medical_id = Column(Integer, ForeignKey('dossiers_medicaux.id'))
    date = Column(Date, nullable=True)
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)

    dossier_medical = relationship("DossierMedical", back_populates="comptes_rendus")
    auteur_id = Column(Integer, ForeignKey('medecins.id'))
    auteur = relationship("Medecin", back_populates="comptes_rendus")
