from sqlalchemy import Column, Integer, String, Date


from src.model.Base import Base

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    birthdate = Column(Date)
    sexe = Column(String(1))