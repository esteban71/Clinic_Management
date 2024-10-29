from faker import Faker
from src.model.CabinetMedical import CabinetMedical
from src.model.Medecin import Medecin
from src.model.Patient import Patient
import numpy as np

fake = Faker()
from sqlalchemy.orm import Session


def create_cabinet_medical(db: Session, nb_cabinet: int):
    cabinet_ids = []
    for _ in range(nb_cabinet):
        cabinet = CabinetMedical(
            name=fake.company(),
            active=True,
            telecom=fake.phone_number(),
            address=fake.address(),
            type=fake.random_element(elements=("hospital", "clinic", "private practice")),
        )
        db.add(cabinet)
        db.flush()
        cabinet_ids.append(cabinet.id)
    db.commit()
    return cabinet_ids


def add_cabinet_to_medecin(db: Session, cabinet_id: list[int] | int, medecin_id: list[int]):
    for i in range(len(medecin_id)):
        medecin = db.query(Medecin).filter(Medecin.id == medecin_id[i]).first()
        if isinstance(cabinet_id, int):
            medecin.cabinet_medical_id = cabinet_id
        else:
            random_cabinet_id = int(np.random.choice(cabinet_id))
        medecin.cabinet_medical_id = random_cabinet_id
    db.commit()

def add_cabinet_to_patient(db: Session, cabinet_id: list[int] | int, patient_id: list[int]):
    for i in range(len(patient_id)):
        patient = db.query(Patient).filter(Patient.id == patient_id[i]).first()
        if isinstance(cabinet_id, int):
            patient.cabinet_medical_id = cabinet_id
        else:
            random_cabinet_id = int(np.random.choice(cabinet_id))
            patient.cabinet_medical_id = random_cabinet_id
    db.commit()
