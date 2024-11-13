import numpy as np
from faker import Faker
from src.model.CabinetMedical import CabinetMedical
from src.model.Medecin import Medecin
from src.model.Patient import Patient

fake = Faker()
from sqlalchemy.orm import Session


def create_cabinet_medical(db: Session, nb_cabinet: int):
    cabinet_ids = []
    for i in range(nb_cabinet):
        cabinet = CabinetMedical(
            name=fake.company(),
            active=True,
            telecom=fake.phone_number(),
            address=fake.address(),
            type=fake.random_element(elements=("hospital", "clinic", "private practice")),
        )
        db.add(cabinet)
    db.commit()
    db.refresh(cabinet)
    cabinet_ids = [cabinet.id for cabinet in db.query(CabinetMedical).all()]
    return cabinet_ids


def add_cabinet_to_medecin(db: Session, cabinet_id: list[int] | int, medecin_id: list[int]):
    for medecin_id_item in medecin_id:
        medecin = db.query(Medecin).filter(Medecin.id == medecin_id_item).first()
        if isinstance(cabinet_id, int):
            medecin.cabinet_medical_id = cabinet_id
        else:
            random_cabinet_id = int(np.random.choice(cabinet_id))
            medecin.cabinet_medical_id = random_cabinet_id
        db.add(medecin)
    db.commit()
    db.refresh(medecin)


def add_cabinet_to_patient(db: Session, cabinet_id: list[int] | int, patient_id: list[int]):
    for patient_id_item in patient_id:
        patient = db.query(Patient).filter(Patient.id == patient_id_item).first()
        if isinstance(cabinet_id, int):
            patient.cabinet_medical_id = cabinet_id
        else:
            random_cabinet_id = int(np.random.choice(cabinet_id))
            patient.cabinet_medical_id = random_cabinet_id
        db.add(patient)
    db.commit()
    db.refresh(patient)
