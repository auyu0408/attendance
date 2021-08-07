from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from attendance.database import get_db
from attendance import schemas
from attendance.models import User
from attendance import crud
from attendance.dependency import get_current_user

router = APIRouter()
##DayOff
#hr
@router.get("/day_off/{id}", response_model= schemas.DayOff, status_code=200)
def dayoff(id: int, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_dayoff(db, date_id=id, current=current_user)

@router.get("/day_off", response_model= List[schemas.DayOff], status_code=200)
def all_dayoff(db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.all_dayoff(db, current=current_user)

@router.post("/day_off", response_model= schemas.DayOff, status_code=201)
def add_dayoff(date_form: schemas.DayOffCreate, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.create_dayoff(db, date=date_form, current=current_user)

@router.delete("/day_off/{id}", response_model= List[schemas.DayOff], status_code=200)
def delete_dayoff(id:int, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.delete_dayoff(db, date_id=id, current=current_user)