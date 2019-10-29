import crud

from fastapi import FastAPI
from db.session import get_db_session
from sqlalchemy.orm import Session

from utils.db import get_db
import models as models
from core import config


app = FastAPI()

print(config.SQLALCHEMY_DATABASE_URI)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/peso")
async def insert_note(
        *,
        db: Session = get_db_session(),
        peso_in: models.peso.PesoCreate):
    
    peso = crud.peso.create(db_session=db, peso_in=peso_in)
    print(peso)