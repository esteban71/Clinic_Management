from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.utils.auth import valid_access_token
from src.app.Patient_routes import router as Patient_router
from src.app.auth_routes import router as auth_router
from src.app.Medecin_routes import router as Medecin_router
from src.database import get_db
from src.test.create_db import create_db , drop_all_data
import os


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


@app.get("/public")
def get_public():
    return {"message": "This endpoint is public"}


@app.get("/private", dependencies=[Depends(valid_access_token)])
def get_private():
    return {"message": "This endpoint is private"}

app.include_router(Patient_router, prefix="/patients")
app.include_router(auth_router, prefix="/auth")
app.include_router(Medecin_router, prefix="/medecins")