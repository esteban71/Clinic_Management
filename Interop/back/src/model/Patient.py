from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


from .Base import Base


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    active = Column(Boolean, nullable=True)  # active status of the patient
    name = Column(String)  # name of the patient
    telecom = Column(String, nullable=True)  # contact details of the patient
    gender = Column(String, nullable=True)  # gender of the patient
    birth_date = Column(Date, nullable=True)  # birth date of the patient
    deceased = Column(JSON, nullable=True)  # deceased status of the patient {deceased: bool, date: date}
    address = Column(String, nullable=True)  # address of the patient
    marital_status = Column(String, nullable=True)  # marital status of the patient
    multiple_birth = Column(Boolean, nullable=True)  # multiple birth status of the patient
    photo = Column(String, nullable=True)  # photo of the patient
    general_practitioner = Column(String, nullable=True)  # general practitioner of the patient
    managing_organization = Column(String, nullable=True)  # managing organization of the patient

    # Relationships
    links = relationship("Link", back_populates="patient", foreign_keys="Link.patient_id")
    contacts = relationship("Contact", back_populates="patient")
    communications = relationship("Communication", back_populates="patient")


class Link(Base):
    __tablename__ = 'links'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    other = Column(Integer, ForeignKey('patients.id'), nullable=True)
    type = Column(String, nullable=True)

    patient = relationship("Patient", back_populates="links")
    other_patient = relationship("Patient", foreign_keys=[other])


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship("Patient", back_populates="contacts", foreign_keys=[patient_id])
    relationship = Column(String, nullable=True)
    role = Column(String, nullable=True)
    name = Column(String, nullable=True)
    additional_name = Column(String, nullable=True)
    telecom = Column(String, nullable=True)
    address = Column(String, nullable=True)
    additional_address = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    organization = Column(String, nullable=True)
    period = Column(String, nullable=True)


class Communication(Base):
    __tablename__ = 'communications'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    language = Column(String, nullable=True)
    preferred = Column(Boolean, nullable=True)

    patient = relationship("Patient", back_populates="communications")