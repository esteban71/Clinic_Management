from faker import Faker
from sqlalchemy.orm import Session
from src.model.Medecin import Medecin

fake = Faker()

def create_medecin(db: Session, nb_medecin: int):
    medecin_ids = []
    medecins = []
    for i in range(nb_medecin):
        medecin = Medecin(
            name=fake.name(),
            rpps=fake.random_number(digits=11),
            specialite=fake.random_element(elements=("generalist", "cardiologist", "dermatologist")),
            email=fake.email(),
            telecom=fake.phone_number(),
            username=fake.user_name(),
        )
        medecins.append(medecin)

    db.add_all(medecins)
    db.commit()
    db.refresh(medecins[-1])
    medecin_ids = [medecin.id for medecin in medecins]  # Collect ids
    return medecin_ids
