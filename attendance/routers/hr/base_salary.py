from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from attendance.database import get_db
from attendance import schemas
from attendance.models import User
from attendance import crud
from attendance.dependency import get_current_user

router = APIRouter()
#BASE_SALARY
#hr
@router.get("/salary/{user_id}", status_code=200)
def read_base_salary(user_id: int, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_base_salarys(db, user_id=user_id, current=current_user)

@router.post("/salary", status_code=201)
def create_base_salary(salary: schemas.BaseSalaryCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.create_base_salary(db, base_salary=salary, current=current_user)
