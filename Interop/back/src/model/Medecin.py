from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from src.model.Base import Base


# https://hl7.org/fhir/practitioner.html

class Medecin(Base):
    __tablename__ = 'medecins'

    id = Column(Integer, primary_key=True, index=True)
    rpps = Column(String, nullable=True)  # référence du professionnel de santé
    name = Column(String, nullable=False)  # Nom du médecin
    specialite = Column(String, nullable=True)  # Spécialité du médecin ici Cardiologue
    email = Column(String, nullable=True)  # Adresse mail
    telecom = Column(String, nullable=True)  # contact
    habilitations = Column(String, nullable=True)  # Organisation ou établissement affilié
    
    
    # Relations    
    patients = relationship("Patient", secondary="Appointment", back_populates="medecins")
    destinataires = relationship("Destinataires", back_populates="medecin")
    secretariat = relationship("Secretariat", back_populates="medecins.id")


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    medecin_id = Column(Integer, ForeignKey('medecins.id'))
    patient_id = Column(Integer, ForeignKey('patients.id'))
    date = Column(Date, nullable=False)  # Date du rendez-vous
    reason = Column(String, nullable=True)  # Raison du rendez-vous

    # Relations
    medecin = relationship("Medecin", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
