from sqlalchemy.orm import Session
from attendance import models, schemas
from fastapi import HTTPException

#utility
def get_base_salarys(db:Session, user_id: int, current: models.User):
    if not current.hr:
        raise HTTPException(status_code=401, detail="You are not hr.")
    return db.query(models.BaseSalary).filter(models.BaseSalary.user_id== user_id)


#hr
def create_base_salary(db:Session, base_salary: schemas.BaseSalaryCreate, current: models.User):
    if not current.hr:
        raise HTTPException(status_code=401, detail="You are not hr.")
    db_salary = models.BaseSalary(salary=base_salary.salary, user_id= base_salary.user_id, date= base_salary.date,
                self_percent= base_salary.self_percent)
    db.add(db_salary)
    db.commit()
    db.refresh(db_salary)
    return db_salary