import logging
from datetime import datetime, timedelta

import numpy as np
from faker import Faker
from sqlalchemy.orm import Session
from src.model.DispositifMedicaux import DispositifMedicaux
from src.model.Dossier import DossierMedical
from src.model.Observation import Observation
from src.model.Patient import Patient

fake = Faker()

logger = logging.getLogger('uvicorn.error')


def create_medical_folder(db: Session, patient_id: int):
    dossier = DossierMedical(
        patient_id=patient_id,
        date_creation=fake.date_of_birth(),
        type_acces=fake.random_element(elements=("public", "private"))
    )
    return dossier


def create_dispositif_medical(db: Session, patient_id: list[int] | int):
    if isinstance(patient_id, int):
        patient_id = [patient_id]
    dispositifs = []
    for i in patient_id:
        dispositif = DispositifMedicaux(
            patient_id=i,
            name=fake.name(),
            type=fake.random_element(
                elements=("Blood Pressure Monitor", "Heart Rate Monitor", "Oxygen Saturation Monitor")),
            interval=fake.random_int(min=1, max=30),
            status="active",
            manufacturer=fake.company(),
            serial_number=fake.random_int(min=1, max=1000),
            lot_number=fake.random_int(min=1, max=1000),
            manufacture_date=fake.date_of_birth(),
            expiration_date=fake.date_of_birth()
        )
        db.add(dispositif)
        db.commit()
        db.refresh(dispositif)
        dispositifs.append(dispositif)
    dispositif_ids = [dispositif.id for dispositif in dispositifs]
    return dispositif_ids


def add_observation_to_dispositif_heart(db: Session, dispositif_id: list[int] | int):
    if isinstance(dispositif_id, int):
        dispositif_id = [dispositif_id]
    for i in dispositif_id:
        dispositif = db.query(DispositifMedicaux).filter(DispositifMedicaux.id == i).first()
        ob = Observation(
            device_id=dispositif_id,
            date_time=datetime.now() + timedelta(days=fake.random_int(min=-10, max=10)),
            code="Heart rate",
            value=fake.random_int(min=30, max=200),
            unit="bpm",
            device=dispositif
        )
        db.add(ob)
        db.commit()
        db.refresh(ob)


def add_observation_to_dispositif_blood(db: Session, dispositif_id: list[int] | int):
    if isinstance(dispositif_id, int):
        dispositif_id = [dispositif_id]
    for i in dispositif_id:
        dispositif = db.query(DispositifMedicaux).filter(DispositifMedicaux.id == i).first()
        ob = Observation(
            device_id=dispositif_id,
            date_time=datetime.now() + timedelta(days=fake.random_int(min=-10, max=10)),
            code="Blood pressure",
            value=fake.random_int(min=60, max=200),
            unit="mmHg",
            component_code=fake.random_element(elements=("systolic", "diastolic")),
            component_value=fake.random_int(min=60, max=200),
            component_unit="mmHg",
            device=dispositif
        )
        db.add(ob)
        db.commit()
        db.refresh(ob)


def add_observation_to_dispositif_oxygen(db: Session, dispositif_id: list[int] | int):
    if isinstance(dispositif_id, int):
        dispositif_id = [dispositif_id]
    for i in dispositif_id:
        dispositif = db.query(DispositifMedicaux).filter(DispositifMedicaux.id == i).first()
        ob = Observation(
            device_id=dispositif_id,
            date_time=datetime.now() + timedelta(days=fake.random_int(min=-10, max=10)),
            code="Oxygen saturation",
            value=fake.random_int(min=60, max=100),
            unit="%",
            device=dispositif
        )
        db.add(ob)
        db.commit()
        db.refresh(ob)


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