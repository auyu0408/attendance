from fastapi import FastAPI, HTTPException, status
from . import models
from .database import SessionLocal, engine
import crud

models.Base.metadata.create_all(bind= engine)

app = FastAPI()

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#@app.get("/users/")
