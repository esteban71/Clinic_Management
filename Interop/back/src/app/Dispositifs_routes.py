import logging
from typing import List

import fhirclient.models.patient as fhir_patient
from fastapi import APIRouter, Depends, HTTPException, Request
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.device import Device, DeviceDeviceName
from fhirclient.models.fhirdatetime import FHIRDateTime
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.identifier import Identifier
from sqlalchemy.orm import Session
from src.database import get_db
from src.model.DispositifMedicaux import DispositifMedicaux
from src.schemas.DispositifMedicauxSchema import DispositifMedicauxSchema, CreateDispositifMedicauxSchema
from src.utils.FHIR import smart_request as smart

logger = logging.getLogger('uvicorn.error')

router = APIRouter()


# Route pour obtenir tous les dossiers médicaux d'un patient
@router.get("/{patient_id}/dispositifs", response_model=List[DispositifMedicauxSchema])
async def get_dispositifs(patient_id: int, db: Session = Depends(get_db)):
    dispositifs = db.query(DispositifMedicaux).filter(DispositifMedicaux.patient_id == patient_id).all()
    return dispositifs


@router.post("/{patient_id}/new", response_model=DispositifMedicauxSchema)
async def create_dispositif(request: Request, patient_id: int, report: CreateDispositifMedicauxSchema,
                            db: Session = Depends(get_db)):
    new_dispositif = DispositifMedicaux(
        patient_id=patient_id,
        name=report.name,
        type=report.type,
        status=report.status,
        manufacturer=report.manufacturer,
        serial_number=report.serial_number,
        lot_number=report.lot_number,
        manufacture_date=report.manufacture_date,
        expiration_date=report.expiration_date,
    )

    db.add(new_dispositif)
    db.commit()
    db.refresh(new_dispositif)
    try:
        device = Device()

        device_name = DeviceDeviceName()
        device_name.name = report.name
        device_name.type = "user-friendly-name"
        device.deviceName = [device_name]

        codeable_concept = CodeableConcept()
        codeable_concept.text = new_dispositif.type
        device.type = codeable_concept

        device.status = new_dispositif.status.lower()

        device.manufacturer = new_dispositif.manufacturer

        device.serialNumber = new_dispositif.serial_number
        device.lotNumber = new_dispositif.lot_number

        device.manufactureDate = FHIRDateTime(new_dispositif.manufacture_date.isoformat())
        device.expirationDate = FHIRDateTime(new_dispositif.expiration_date.isoformat())

        identifier = Identifier()
        identifier.system = "backend"
        identifier.value = str(new_dispositif.id)
        device.identifier = [identifier]

        identifier_system = "backend"
        identifier_value = patient_id
        search_resource = fhir_patient.Patient.where(
            struct={"identifier": f"{identifier_system}|{identifier_value}"}).perform(
            smart().server)
        if search_resource is None:
            return db_patient
        fhir_patient_resource = fhir_patient.Patient.read(search_resource.entry[0].resource.id, smart().server)

        device.patient = FHIRReference({"reference": f"Patient/{fhir_patient_resource.id}"})

        device.create(smart().server)
    except Exception as e:
        logger.error(f"Error creating device: {e}")
        return new_dispositif

    return new_dispositif


@router.patch("/{patient_id}/dispositif/{dispositif_id}", response_model=DispositifMedicauxSchema)
async def update_dispositifs(patient_id: int, dispositif_id: int, report: CreateDispositifMedicauxSchema,
                             db: Session = Depends(get_db)):
    dispositif = db.query(DispositifMedicaux).filter(
        DispositifMedicaux.id == dispositif_id
    ).first()

    if not dispositif:
        raise HTTPException(status_code=404, detail="Medical device not found")

    dispositif.name = report.name
    dispositif.type = report.type
    dispositif.interval = report.interval
    dispositif.status = report.status
    dispositif.manufacturer = report.manufacturer
    dispositif.serial_number = report.serial_number
    dispositif.lot_number = report.lot_number
    dispositif.manufacture_date = report.manufacture_date
    dispositif.expiration_date = report.expiration_date
    db.commit()
    db.refresh(dispositif)

    try:

        search_device = Device.where(struct={"identifier": f"backend|{dispositif_id}"}).perform(smart().server)

        device = Device.read(search_device.entry[0].resource.id, smart().server)

        device_name = DeviceDeviceName()
        device_name.name = report.name
        device_name.type = "user-friendly-name"
        device.deviceName = [device_name]

        codeable_concept = CodeableConcept()
        codeable_concept.text = dispositif.type
        device.type = codeable_concept

        device.status = dispositif.status.lower()

        device.manufacturer = dispositif.manufacturer

        device.serialNumber = dispositif.serial_number
        device.lotNumber = dispositif.lot_number

        device.manufactureDate = FHIRDateTime(dispositif.manufacture_date.isoformat())
        device.expirationDate = FHIRDateTime(dispositif.expiration_date.isoformat())

        device.update(smart().server)
    except Exception as e:
        logger.error(f"Error updating device: {e}")
        return dispositif

    return dispositif


# Route pour supprimer un rapport médical d'un patient
@router.delete("/{patient_id}/dispositif/{dispositif_id}")
async def delete_dispositifs(patient_id: int, dispositif_id: int, db: Session = Depends(get_db)):
    dispositif = db.query(DispositifMedicaux).filter(
        DispositifMedicaux.id == dispositif_id,
    ).first()

    if not dispositif:
        raise HTTPException(status_code=404, detail="Medical device not found")

    db.delete(dispositif)
    db.commit()

    try:
        search_device = Device.where(struct={"identifier": f"backend|{dispositif_id}"}).perform(smart().server)

        device = Device.read(search_device.entry[0].resource.id, smart().server)
        device.delete(smart().server)
    except Exception as e:
        logger.error(f"Error deleting device: {e}")
        return {"message": "Medical device deleted successfully"}

    return {"message": "Medical device deleted successfully"}
