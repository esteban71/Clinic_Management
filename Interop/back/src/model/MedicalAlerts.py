from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from src.model.Base import Base


class AlerteMedicale(Base):
    __tablename__ = 'alertes_medicales'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=True)  # date of the alert
    type = Column(String, nullable=True)  # type of the alert
    description = Column(String, nullable=True)  # description of the alert
    destinataires = Column(String, nullable=True)  # recipients of the alert
    status = Column(String, nullable=True)  # status of the alert

    patient = relationship("Patient", back_populates="alertes_medicales")
    destinataires = relationship("Destinataires", back_populates="alerte")
    mesures_cardiaques = relationship("MesuresCardiaques", back_populates="alerte")


class Destinataires(Base):
    __tablename__ = 'destinataires'

    id = Column(Integer, primary_key=True)
    medecin_referecence = Column(Integer, ForeignKey('medecins.id'))
    urgences = Column(Boolean, nullable=True)
    contactUrgence = Column(String, nullable=True)
    alerte_id = Column(Integer, ForeignKey('alertes_medicales.id'))

    alerte = relationship("AlerteMedicale", back_populates="destinataires", foreign_keys=[alerte_id])
    medecin = relationship("Medecin", back_populates="destinataires")


class MesuresCardiaques(Base):
    __tablename__ = 'mesures_cardiaques'

    id = Column(Integer, primary_key=True)
    tension_arterielle = Column(String, nullable=True)
    rythme_cardiaque = Column(String, nullable=True)
    oxyometrie = Column(String, nullable=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    
    alerte = relationship("AlerteMedicale", back_populates="mesures_cardiaques")
    patient = relationship("Patient", back_populates="mesures_cardiaques", foreign_keys=[patient_id])