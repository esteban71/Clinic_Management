from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from src.model.Base import Base


class DispositifMedical(Base):
    __tablename__ = 'dispositifs_medicaux'

    id = Column(Integer, primary_key=True)
    type = Column(String)  # type of the medical device
    patient_id = Column(Integer, ForeignKey('patients.id'))
    interval = Column(Integer, nullable=True)  # interval of the medical device
    status = Column(String, nullable=True)  # status of the medical device

    # Relationships
    patient = relationship("Patient", back_populates="dispositifs_medicaux")
    donnees_medicales = relationship("DonneeMedicale", back_populates="dispositif_medical")


class DonneeMedicale(Base):
    __tablename__ = 'donnees_medicales'

    id = Column(Integer, primary_key=True)
    date = Column(Date)  # date of the medical data
    type = Column(String)  # type of the medical data
    valeur = Column(String)  # value of the medical data
    unite = Column(String, nullable=True)  # unit of the medical data
    mesures = Column(String, nullable=True)  # measures of the medical data

    # Relationships
    dispositif_medical = relationship("DispositifMedical", back_populates="donnees_medicales")
    patient = relationship("Patient", back_populates="donnees_medicales")
