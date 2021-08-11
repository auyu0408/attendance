from typing import List
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from attendance.database import get_db
from attendance import schemas
from attendance.models import User
from attendance import crud
from attendance.dependency import get_current_user

router = APIRouter()

@router.get("/daily", status_code=200)
def hr_daily_list(db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.all_daily(db, current=current_user)

@router.get("/daily/{id}", status_code=200)
def hr_daily(id:int, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_daily(db, current=current_user, id=id)

@router.post("/daily", status_code=201)
def add_daily(daily_form: schemas.DailyCreate, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.create_daily(db, daily= daily_form, current=current_user)

@router.put("/daily/{id}", status_code=200)
def update_daily(id: int, daily_form: schemas.DailyUpdate, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.update_daily(db, daily=daily_form, daily_id=id, current=current_user)