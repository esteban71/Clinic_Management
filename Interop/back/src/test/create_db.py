from sqlalchemy import text
from src.database import SessionLocal
from src.test.create_cabinet_medical import create_cabinet_medical, add_cabinet_to_medecin, add_cabinet_to_patient
from src.test.create_medecin import create_medecin
from src.test.create_patient import create_patient, add_medecin_to_patient

all_tables = ["secretariat", "comptes_rendus_medicaux", "dossiers_medicaux", "patients", "medecins", "cabinet_medical"]


def drop_all_data():
    with SessionLocal() as db:
        for table in all_tables:
            db.execute(text(f"DELETE FROM {table}"))
        db.commit()


def create_db():
    with SessionLocal() as db:
        patient_ids = create_patient(db, 10);
        medecin_ids = create_medecin(db, 10);
        cabinet_ids = create_cabinet_medical(db, 10);
        add_cabinet_to_medecin(db, cabinet_ids, medecin_ids)
        add_medecin_to_patient(db, medecin_ids, patient_ids)
        add_cabinet_to_patient(db, cabinet_ids, patient_ids)
