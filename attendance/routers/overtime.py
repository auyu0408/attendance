from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from attendance.database import get_db
from attendance import schemas
from attendance.models import User
from attendance import crud
from attendance.dependency import get_current_user

router = APIRouter()

#LEAVE
#self
@router.get("/overtime", response_model=List[schemas.Leave], status_code=200)
def overtime_list(db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_overtimes(db, user_id=current_user.id)

@router.get("/overtime/{id}", response_model= schemas.Leave, status_code=200)
def read_overtime(id: int, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_overtime(db, id=id, current=current_user)

@router.post("/overtime", response_model=schemas.Overtime, status_code=201)
def add_overtime(overtime_form: schemas.OvertimeCreate, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.create_overtime(db, Overtime=overtime_form, user_id=current_user.id)

@router.put("/overtime/{id}", response_model=schemas.Overtime, status_code=200)
def update_overtime(id: int, overtime_from: schemas.OvertimeCreate, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.update_overtime(db, Overtime=overtime_from, current=current_user, id=id)

#manager
@router.get("/check_leave", response_model=List[schemas.Leave], status_code=200)
def check_overtime_list(db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_other_overtimes(db, current=current_user)

@router.put("/check_leave/{id}", response_model=schemas.Leave, status_code=200)
def check_overtime(id: int, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.check_overtime(db, overtime_id=id, current=current_user)