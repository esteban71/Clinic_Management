import asyncio

from sqlalchemy import text
from sqlalchemy.orm import Session
from src.model import Patient, DispositifMedicaux
from src.test.create_cabinet_medical import create_cabinet_medical, add_cabinet_to_medecin, add_cabinet_to_patient
from src.test.create_medecin import create_medecin
from src.test.create_patient import create_patient, add_medecin_to_patient, add_observation_to_dispositif_heart, \
    create_dispositif_medical, add_observation_to_dispositif_blood, add_observation_to_dispositif_oxygen

all_tables = ["secretariat", "observations", "dispositif_medicaux", "comptes_rendus_medicaux", "dossiers_medicaux",
              "patients", "medecins", "cabinet_medical"]


def drop_all_data(db: Session):
    for table in all_tables:
        db.execute(text(f"DELETE FROM {table}"))
    db.commit()


def create_db(db: Session):
    patient_ids = create_patient(db, 10);
    medecin_ids = create_medecin(db, 10);
    cabinet_ids = create_cabinet_medical(db, 10);
    add_cabinet_to_medecin(db, cabinet_ids, medecin_ids)
    add_medecin_to_patient(db, medecin_ids, patient_ids)
    add_cabinet_to_patient(db, cabinet_ids, patient_ids)
    dispositif_ids = create_dispositif_medical(db, patient_ids)
    start_observation_task(db)


async def add_observations_periodically(db: Session):
    while True:
        patient_ids = [patient.id for patient in db.query(Patient).all()]
        dispositif_ids = dispositif_ids = [dispositif.id for dispositif in db.query(DispositifMedicaux).all() if
                                           dispositif.status == "active" and dispositif.type == "Heart Rate Monitor"]
        add_observation_to_dispositif_heart(db, dispositif_ids)
        dispositif_ids = [dispositif.id for dispositif in db.query(DispositifMedicaux).all() if
                          dispositif.status == "active" and dispositif.type == "Blood Pressure Monitor"]
        add_observation_to_dispositif_blood(db, dispositif_ids)
        dispositif_ids = [dispositif.id for dispositif in db.query(DispositifMedicaux).all() if
                          dispositif.status == "active" and dispositif.type == "Oxygen Saturation Monitor"]
        add_observation_to_dispositif_oxygen(db, dispositif_ids)

        await asyncio.sleep(60)


def start_observation_task(db: Session):
    loop = asyncio.get_event_loop()
    loop.create_task(add_observations_periodically(db))
