from fastapi import FastAPI, Depends

from src.utils.auth import valid_access_token
from src.app.Patient_routes import router as Patient_router

app = FastAPI()

@app.get("/public")
def get_public():
    return {"message": "This endpoint is public"}


@app.get("/private", dependencies=[Depends(valid_access_token)])
def get_private():
    return {"message": "This endpoint is private"}


app.include_router(Patient_router, prefix="/patient")

