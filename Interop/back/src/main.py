import os

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.app.Medecin_routes import router as Medecin_router
from src.app.Patient_routes import router as Patient_router
from src.app.auth_routes import router as auth_router
from src.test.create_db import create_db, drop_all_data
from src.utils.auth import protected_route

env = os.getenv("ENV", "dev")

def create_app():
    if env == "dev":
        drop_all_data()
        app = FastAPI()
        create_db()
    elif env == "prod":
        app = FastAPI()
    return app

app = create_app()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Patient_router, prefix="/patients",
                   dependencies=[Depends(protected_route(["admin", "Doctor", "Receptionist"]))])
app.include_router(auth_router, prefix="/auth")
app.include_router(Medecin_router, prefix="/medecins",
                   dependencies=[Depends(protected_route(["admin", "Receptionist"]))])
