from attendance.main import get_current_user, get_db
from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from attendance import models, schemas
from attendance import crud
from fastapi import APIRouter

salary_router = APIRouter()
#BASE_SALARY
#hr
@salary_router.get("/hr/salary/{id}", response_model = List[schemas.BaseSalary], status_code=200)
def read_base_salary(id: int, current_user: models.User=Depends(get_current_user), db: Session=Depends(get_db)):
    if not current_user.hr:
        raise HTTPException(status_code=401, detail="Your are not hr.")
    return crud.get_base_salarys(db, user_id=id)

@salary_router.post("/hr/salary/", status_code=201, response_model= List[schemas.BaseSalary])
def create_base_salary(salary: schemas.BaseSalaryCreate, db: Session = Depends(), current_user: models.User=Depends()):
    if not current_user.hr:
        raise HTTPException(status_code=401, detail="Your are not hr.")
    crud.create_salary(db, base_salary=salary)
    return crud.get_base_salarys(db, user_id=salary.user_id)
