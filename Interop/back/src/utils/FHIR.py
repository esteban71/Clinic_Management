import os

import fhirclient.models.patient as fhir_patient
from fhirclient import client

settings = {
    'app_id': os.environ.get("APP_ID"),
    'api_base': os.environ.get("API_BASE_URL"),
}


def smart_request():
    return client.FHIRClient(settings=settings)


from fhirclient.models.fhirreference import FHIRReference


def add_practitioner_to_patient(patient_id, practitioner_id):
    # Read the existing Patient resource
    fhir_patient_resource = fhir_patient.Patient.read(patient_id.entry[0].resource.id, smart_request().server)
    fhir_patient_resource.id = fhir_patient_resource.id

    # Create a reference to the Practitioner
    practitioner_reference = FHIRReference()
    practitioner_reference.reference = f"Practitioner/{practitioner_id}"

    # Add the Practitioner reference to the Patient's generalPractitioner field
    if fhir_patient_resource.generalPractitioner:
        fhir_patient_resource.generalPractitioner.append(practitioner_reference)
    else:
        fhir_patient_resource.generalPractitioner = [practitioner_reference]

    # Update the Patient resource on the FHIR server
    fhir_patient_resource.update(smart_request().server)
