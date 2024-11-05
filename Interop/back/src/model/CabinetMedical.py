from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from src.model.Base import Base


class CabinetMedical(Base):
    __tablename__ = 'cabinet_medical'

    id = Column(Integer, primary_key=True)
    active = Column(Boolean, nullable=True)  # active status of the cabinet
    name = Column(String)  # name of the cabinet
    telecom = Column(String, nullable=True)  # contact details of the cabinet
    address = Column(String, nullable=True)  # address of the cabinet
    type = Column(String, nullable=True)  # type of the cabinet

    # Relationships

    medecins = relationship("Medecin", back_populates="cabinet_medical")
    patients = relationship("Patient", back_populates="cabinet_medical")
    secretariat = relationship("Secretariat", back_populates="cabinet_medical")