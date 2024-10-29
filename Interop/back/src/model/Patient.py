from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from .Base import Base


# https://hl7.org/fhir/patient.html

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    active = Column(Boolean, nullable=True)  # active status of the patient
    name = Column(String)  # name of the patient
    telecom = Column(String, nullable=True)  # contact details of the patient
    gender = Column(String, nullable=True)  # gender of the patient
    birth_date = Column(Date, nullable=True)  # birth date of the patient
    address = Column(String, nullable=True)  # address of the patient
    marital_status = Column(String, nullable=True)  # marital status of the patient
    managing_organization = Column(String, nullable=True)  # managing organization of the patient
    medecin_id = Column(Integer, ForeignKey('medecins.id'), nullable=True)  # medecin of the patient

    # Relationships
    links = relationship("Link", back_populates="patient", foreign_keys="Link.patient_id")
    contacts = relationship("Contact", back_populates="patient")

    cabinet_medical_id = Column(Integer, ForeignKey('cabinet_medical.id'))
    cabinet_medical = relationship("CabinetMedical", back_populates="patients")
    dossier_medical = relationship("DossierMedical", back_populates="patient", uselist=False)
    dossier_administratif = relationship("DossierAdministratif", back_populates="patient", uselist=False)
    dispositifs_medicaux = relationship("DispositifMedical", back_populates="patient")
    alertes_medicales = relationship("AlerteMedicale", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")

class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    other = Column(Integer, ForeignKey('patients.id'), nullable=True)
    type = Column(String, nullable=True)

    patient = relationship("Patient", back_populates="links", foreign_keys=[patient_id])
    other_patient = relationship("Patient", foreign_keys=[other])


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship("Patient", back_populates="contacts", foreign_keys=[patient_id])
    relationship = Column(String, nullable=True)
    name = Column(String, nullable=True)
    additional_name = Column(String, nullable=True)
    telecom = Column(String, nullable=True)
    address = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    organization = Column(String, nullable=True)