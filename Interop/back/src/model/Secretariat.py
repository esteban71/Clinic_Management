from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from src.model.Base import Base

class Secretariat(Base):
    __tablename__ = 'secretariat'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)  # name of the secretariat
    email = Column(String, nullable=True)  # email of the secretariat
    telephone = Column(String, nullable=True)  # telephone of the secretariat
    habilitations = Column(String, nullable=True)  # habilitations of the secretariat
    
    # Relationships
    cabinet_medical = relationship("CabinetMedical", back_populates="secretariat")