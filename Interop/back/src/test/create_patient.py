import numpy as np
from faker import Faker
from sqlalchemy.orm import Session
from src.model.Dossier import DossierMedical
from src.model.Patient import Patient

fake = Faker()


def create_medical_folder(db: Session, patient_id: int):
    dossier = DossierMedical(
        patient_id=patient_id,
        date_creation=fake.date_of_birth(),
        type_acces=fake.random_element(elements=("public", "private"))
    )
    return dossier


def create_patient(db: Session, nb_patient: int):
    patient_ids = []
    dossiers = []
    patients = []

    for i in range(nb_patient):
        dossier_medical = create_medical_folder(db, i)
        dossiers.append(dossier_medical)  # Add to list

        patient = Patient(
            name=fake.name(),
            active=fake.boolean(),
            telecom=fake.phone_number(),
            gender=fake.random_element(elements=("male", "female")),
            birth_date=fake.date_of_birth(),
            address=fake.address(),
            marital_status=fake.random_element(elements=("single", "married", "divorced")),
            dossier_medical=dossier_medical
        )
        patients.append(patient)

    db.add_all(dossiers)
    db.add_all(patients)
    db.commit()
    patient_ids = [patient.id for patient in patients]
    db.refresh(patients[-1])
    db.refresh(dossiers[-1])
    return patient_ids


def add_medecin_to_patient(db: Session, medecin_id: list[int] | int, patient_id: list[int]):
    for i in range(len(patient_id)):
        patient = db.query(Patient).filter(Patient.id == patient_id[i]).first()
        if isinstance(medecin_id, int):
            patient.medecin_id = medecin_id
        else:
            random_medecin_id = int(np.random.choice(medecin_id))
            patient.medecin_id = random_medecin_id
    db.commit()
    db.refresh(patient)
