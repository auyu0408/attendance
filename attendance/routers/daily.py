from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from attendance.database import get_db
from attendance import schemas
from attendance.models import User
from attendance import crud
from attendance.dependency import get_current_user

router = APIRouter()

##Daily
#self
@router.get("/daily/{id}", response_model= schemas.Daily, status_code=200)
def read_daily(id: int, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_daily(db, id=id, current=current_user)

@router.get("/daily", response_model= List[schemas.Daily], status_code=200)
def daily_list(db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_dailys(db, user_id=current_user.id)

@router.put("/daily/{id}", response_model=schemas.Daily, status_code=200)
def update_daily(id: int, daily_form: schemas.DailyUpdate, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.update_daily(db, daily=daily_form, daily_id=id, current=current_user)