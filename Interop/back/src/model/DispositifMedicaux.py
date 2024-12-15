from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from src.model.Base import Base


class DispositifMedicaux(Base):
    __tablename__ = 'dispositif_medicaux'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)  # name of the medical device
    type = Column(String, nullable=True)  # type of the medical device
    interval = Column(Integer, nullable=True)  # interval of use
    status = Column(String, nullable=True)  # status of the device
    manufacturer = Column(String, nullable=True)  # manufacturer of the device
    serial_number = Column(String, nullable=True)  # serial number of the device
    lot_number = Column(String, nullable=True)  # lot number of the device
    manufacture_date = Column(Date, nullable=True)  # manufacture date of the device
    expiration_date = Column(Date, nullable=True)  # expiration date of the device

    patient_id = Column(Integer, ForeignKey('patients.id'))
    patient = relationship("Patient", back_populates="dispositif_medicaux")

    observations = relationship("Observation", back_populates="device", uselist=True)
