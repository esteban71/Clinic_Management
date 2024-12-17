from faker import Faker
from fhirclient.models.address import Address
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.contactpoint import ContactPoint
from fhirclient.models.humanname import HumanName
from fhirclient.models.identifier import Identifier
from fhirclient.models.practitioner import Practitioner
from sqlalchemy.orm import Session
from src.model.Medecin import Medecin
from src.utils.FHIR import smart_request as smart

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
        db.add(medecin)
        db.commit()
        db.refresh(medecin)
        try:
            practitioner = Practitioner()
            name = HumanName()
            name.given = [str(medecin.name)]
            practitioner.name = [name]

            contact = ContactPoint()
            contact.system = "phone"
            contact.value = str(medecin.telecom)
            contact.use = "work"

            contact2 = ContactPoint()
            contact2.system = "email"
            contact2.value = str(medecin.email)
            contact2.use = "work"

            practitioner.telecom = [contact, contact2]

            address = Address()
            address.line = ["Test"]

            practitioner.address = [address]

            identifier = Identifier()
            identifier.system = "backend"
            identifier.value = str(medecin.id)

            practitioner.identifier = [identifier]

            code = CodeableConcept()
            code.text = "cardiologist"

            practitioner.practitionerRole = [{"specialty": [code]}]

            practitioner.create(smart().server)
        except Exception as e:
            logger.info(f"Error creating practitioner: {e}")
            continue


    db.refresh(medecins[-1])
    medecin_ids = [medecin.id for medecin in medecins]  # Collect ids
    return medecin_ids
