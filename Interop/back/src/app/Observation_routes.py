import logging
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.device import Device
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.observation import Observation as FHIRObservation
from fhirclient.models.quantity import Quantity
from sqlalchemy.orm import Session
from src.database import get_db
from src.model.DispositifMedicaux import DispositifMedicaux
from src.model.Observation import Observation
from src.schemas.ObservationSchema import CreateObservationSchema, ObservationSchema
from src.utils.FHIR import smart_request as smart

logger = logging.getLogger('uvicorn.error')

router = APIRouter()


@router.get("/{patient_id}/observations", response_model=List[ObservationSchema])
async def get_observations(patient_id: int, db: Session = Depends(get_db)):
    dispositif_medical = db.query(DispositifMedicaux).filter(DispositifMedicaux.patient_id == patient_id).first()
    if not dispositif_medical:
        raise HTTPException(status_code=404, detail="dispositif médical not found")
    observations = db.query(Observation).filter(Observation.device_id == dispositif_medical.id).all()
    if not observations:
        return []
    return observations


@router.post("/{patient_id}/observations/new", response_model=CreateObservationSchema)
async def create_observations(request: Request, patient_id: int, report: CreateObservationSchema,
                              db: Session = Depends(get_db)):
    dispositif_medical = db.query(DispositifMedicaux).filter(DispositifMedicaux.patient_id == patient_id).first()

    if not dispositif_medical:
        raise HTTPException(status_code=404, detail="Medical device not found")

    new_observation = Observation(
        date_time=datetime.now(),
        code=report.title,
        value=report.content,
        unit=report.unit,
        status="final",
        patient_id=patient_id,
        device_id=dispositif_medical.id,
        component_code=report.component_code,
        component_value=report.component_value,
        component_unit=report.component_unit
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    try:
        fhir_observation = FHIRObservation()
        fhir_observation.status = new_observation.status

        codeable_concept = CodeableConcept()
        codeable_concept.text = new_observation.code

        fhir_observation.code = codeable_concept

        search_device = Device.where(struct={"identifier": f"backend|{dispositif_medical.id}"}).perform(
            smart().server)

        device = Device.read(search_device.entry[0].resource.id, smart().server)
        fhir_observation.subject = FHIRReference({"reference": f"Device/{device.id}"})
        # fhir_observation.issued = FHIRDateTime(new_observation.date_time.isoformat())
        quantity = Quantity()
        quantity.value = new_observation.value
        quantity.unit = new_observation.unit
        fhir_observation.valueQuantity = quantity

        if new_observation.component_code:
            component_codeable_concept = CodeableConcept()
            component_codeable_concept.text = new_observation.component_code
            component = ObservationComponent()
            component.code = component_codeable_concept

            component_quantity = Quantity()
            component_quantity.value = new_observation.component_value
            component_quantity.unit = new_observation.component_unit
            component.valueQuantity = component_quantity

            fhir_observation.component = [component]

        fhir_observation.create(smart().server)

    except Exception as e:
        logger.error(f"Error creating FHIR observation: {e}")
        return new_report

    return new_report


# Route pour supprimer un rapport médical d'un patient
@router.delete("/{patient_id}/observations/{report_id}")
async def delete_observations(patient_id: int, report_id: int, db: Session = Depends(get_db)):
    observation = db.query(Observation).filter(Observation.id == report_id).first()

    if not observation:
        raise HTTPException(status_code=404, detail="Medical report not found")

    db.delete(observation)
    db.commit()
    try:
        search_observation = Observation.where(struct={"identifier": f"backend|{observation.id}"}).perform(
            smart().server)

        observation = Observation.read(search_observation.entry[0].resource.id, smart().server)
        observation.delete(smart().server)
    except Exception as e:
        logger.error(f"Error deleting observation: {e}")
        return {"message": "Medical report deleted successfully"}

    return {"message": "Medical report deleted successfully"}
