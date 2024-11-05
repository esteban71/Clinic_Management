from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.model.Base import Base


class Secretariat(Base):
    __tablename__ = 'secretariat'

    id = Column(Integer, primary_key=True)
    name = Column(String)  # name of the secretariat
    username = Column(String, nullable=True)  # Nom d'utilisateur dans keycloak
    email = Column(String, nullable=True)  # email of the secretariat
    telephone = Column(String, nullable=True)  # telephone of the secretariat
    habilitations = Column(String, nullable=True)  # habilitations of the secretariat
    medecin_id = Column(Integer, ForeignKey('medecins.id'), nullable=True)  # medecin of the secretariat
    cabinet_medical_id = Column(Integer, ForeignKey('cabinet_medical.id'), nullable=False)  # cabinet_medical of the secretariat

    # Relationships
    cabinet_medical_id = Column(Integer, ForeignKey('cabinet_medical.id'))
    cabinet_medical = relationship("CabinetMedical", back_populates="secretariat")