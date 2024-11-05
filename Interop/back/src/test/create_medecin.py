from faker import Faker
from src.model.Medecin import Medecin

fake = Faker()
from sqlalchemy.orm import Session


def create_medecin(db: Session, nb_medecin: int):
    medecin_ids = []
    for _ in range(nb_medecin):
        medecin = Medecin(
            name=fake.name(),
            rpps=fake.random_number(digits=11),
            specialite=fake.random_element(elements=("generalist", "cardiologist", "dermatologist")),
            email=fake.email(),
            telecom=fake.phone_number(),
        )
        db.add(medecin)
        db.flush()
        medecin_ids.append(medecin.id)
    db.commit()
    return medecin_ids
