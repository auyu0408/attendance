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
@router.get("/hr/salary/{user_id}", response_model = List[schemas.BaseSalary], status_code=200)
def read_base_salary(user_id: int, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_base_salarys(db, user_id=id, current=current_user)

@router.post("/hr/salary/", status_code=201, response_model= List[schemas.BaseSalary])
def create_base_salary(salary: schemas.BaseSalaryCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    crud.create_salary(db, base_salary=salary, current=current_user)
    return crud.get_base_salarys(db, user_id=salary.user_id, current=current_user)
