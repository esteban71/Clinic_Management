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
    patient_id = Column(Integer, ForeignKey('patients.id'))

    patient = relationship("Patient", back_populates="alertes_medicales")
    destinataires = relationship("Destinataires", back_populates="alerte")


class Destinataires(Base):
    __tablename__ = 'destinataires'

    id = Column(Integer, primary_key=True)
    medecin_referecence = Column(Integer, ForeignKey('medecins.id'))
    urgences = Column(Boolean, nullable=True)
    contactUrgence = Column(String, nullable=True)
    alerte_id = Column(Integer, ForeignKey('alertes_medicales.id'))

    alerte = relationship("AlerteMedicale", back_populates="destinataires")
    medecin = relationship("Medecin", back_populates="destinataires")


class MesuresCardiaques(Base):
    __tablename__ = 'mesures_cardiaques'

    id = Column(Integer, primary_key=True)
    tension_arterielle = Column(String, nullable=True)
    rythme_cardiaque = Column(String, nullable=True)
    oxyometrie = Column(String, nullable=True)
    
    donnee_medicale_id = Column(Integer, ForeignKey('donnees_medicales.id'))
    donnee_medicale = relationship("DonneeMedicale", back_populates="mesures_cardiaques")