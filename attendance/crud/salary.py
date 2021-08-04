from attendance.schemas import salary, user
from salalchemy.orm import Session
from . import models, schemas

#utility
def get_salarys(db:Session, user_id: int):
    return db.query(models.Salary).filter(models.Salary.user_id== user_id)

#hr
def create_salary(db:Session, salary: schemas.SalaryCreate):
    db_salary = models.Salary(salary=salary.salary, user_id= salary.user_id, date= salary.date,
                self_percent= salary.self_percent)
    db.add(db_salary)
    db.commit()
    db.refresh(db_salary)
    return db_salary