from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.model.Base import Base


# https://hl7.org/fhir/practitioner.html

class Medecin(Base):
    __tablename__ = 'medecins'

    id = Column(Integer, primary_key=True, index=True)
    rpps = Column(String, nullable=True)  # référence du professionnel de santé
    name = Column(String, nullable=False)  # Nom du médecin
    username = Column(String, nullable=True)  # Nom d'utilisateur dans keycloak
    specialite = Column(String, nullable=True)  # Spécialité du médecin ici Cardiologue
    email = Column(String, nullable=True)  # Adresse mail
    telecom = Column(String, nullable=True)  # contact
    #habilitations = Column(String, nullable=True)  # Organisation ou établissement affilié
    
    
    # Relations    
    cabinet_medical_id = Column(Integer, ForeignKey('cabinet_medical.id'))
    cabinet_medical = relationship("CabinetMedical", back_populates="medecins")
    comptes_rendus = relationship("CompteRenduMedical", back_populates="auteur")
    patients = relationship("Patient", back_populates="medecin")
