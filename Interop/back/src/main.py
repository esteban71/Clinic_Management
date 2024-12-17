import os

from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from src.app.Dispositifs_routes import router as Dispositif_router
from src.app.Dossier_routes import router as Dossier_router
from src.app.Medecin_routes import router as Medecin_router
from src.app.Observation_routes import router as Observation_router
from src.app.Patient_routes import router as Patient_router
from src.app.Secretariat_routes import router as Secretariat_router
from src.app.auth_routes import router as auth_router
from src.app.cabinet_routes import router as Cabinet_router
from src.database import SessionLocal
from src.test.create_db import create_db
from src.utils.auth import protected_route

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    env = os.getenv("ENV", "dev")
    if env == "dev":
        with SessionLocal() as db:
            # drop_all_data(db)
            create_db(db)


app.include_router(Patient_router, prefix="/patients",
                   dependencies=[Security(protected_route(["admin", "Doctor", "Receptionist"]))])
app.include_router(auth_router, prefix="/auth")

app.include_router(Medecin_router, prefix="/medecins",
                   dependencies=[Security(protected_route(["admin", "Receptionist"]))])

app.include_router(Dossier_router, prefix="/dossier",
                   dependencies=[Security(protected_route(["admin", "Doctor"]))])

app.include_router(Observation_router, prefix="/dispositifs",
                   dependencies=[Security(protected_route(["admin", "Doctor", "Dispositif"]))])

app.include_router(Dispositif_router, prefix="/dispositifs",
                   dependencies=[Security(protected_route(["admin", "Doctor", "Dispositif"]))])

app.include_router(Cabinet_router, prefix="/cabinets",
                   dependencies=[Security(protected_route(["admin", "Receptionist", "Doctor"]))])

app.include_router(Secretariat_router, prefix="/receptionists",
                   dependencies=[Security(protected_route(["admin"]))])
