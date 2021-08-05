from sqlalchemy.orm import Session
from attendance import models, schemas

#utility
def get_base_salarys(db:Session, user_id: int):
    return db.query(models.BaseSalary).filter(models.BaseSalary.user_id== user_id)

#hr
def create_base_salary(db:Session, base_salary: schemas.BaseSalaryCreate):
    db_salary = models.BaseSalary(salary=base_salary.salary, user_id= base_salary.user_id, date= base_salary.date,
                self_percent= base_salary.self_percent)
    db.add(db_salary)
    db.commit()
    db.refresh(db_salary)
    return db_salary