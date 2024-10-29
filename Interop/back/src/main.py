from fastapi import FastAPI, Depends

from src.utils.auth import valid_access_token
from src.app.Patient_routes import router as Patient_router
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

@app.get("/public")
def get_public():
    return {"message": "This endpoint is public"}


@app.get("/private", dependencies=[Depends(valid_access_token)])
def get_private():
    return {"message": "This endpoint is private"}


app.include_router(Patient_router, prefix="/patient")

