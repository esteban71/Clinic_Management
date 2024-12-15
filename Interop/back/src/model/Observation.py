from sqlalchemy import Column, Integer, Float, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from src.model.Base import Base


class Observation(Base):
    __tablename__ = 'observations'

    id = Column(Integer, primary_key=True)
    date_time = Column(DateTime, nullable=True)  # Date and time of the observation
    code = Column(String, nullable=True)  # Observation type (e.g., "Blood Pressure", "Heart Rate")
    value = Column(Float, nullable=True)  # Value of the observation
    unit = Column(String, nullable=True)  # Unit of the observation (e.g., "mmHg", "bpm")
    status = Column(String, default="final")  # Status of the observation ("final", "amended", etc.)

    # For composite observations (e.g., blood pressure with systolic and diastolic)
    component_code = Column(String, nullable=True)  # Sub-code for the component (e.g., "systolic", "diastolic")
    component_value = Column(Float, nullable=True)  # Value for the component
    component_unit = Column(String, nullable=True)  # Unit for the component

    # Relationships

    device_id = Column(Integer, ForeignKey('dispositif_medicaux.id'))  # Reference to the device

    device = relationship("DispositifMedicaux", back_populates="observations")
