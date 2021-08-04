from attendance.schemas import user
from salalchemy.orm import Session
from . import models, schemas

#self
def create_overtime(db:Session, Overtime: schemas.OvertimeCreate, user_id: int):
    db_overtime = models.Overtime(day= Overtime.day, start= Overtime.start, end= Overtime.end, 
                        reason= Overtime.str, check= False, user_id = user_id)
    db.add(db_overtime)
    db.commit()
    db.refresh(db_overtime)
    return db_overtime

def update_overtime(db:Session, Overtime: schemas.Overtime):
    db_overtime = db.query(models.Overtime).filter(models.Overtime.id == Overtime.id)
    db_overtime.update({
        "day": Overtime.day,
        "start": Overtime.start, 
        "end": Overtime.end, 
        "reason": Overtime.reason,
        "check": False
    })
    db.commit()
    return db_overtime

#utility
def get_overtime(db:Session, id: int):
    return db.query(models.Overtime).filter(models.Overtime.id == id).first()

def get_overtimes(db:Session, user_id: int):
    return db.query(models.Overtime).filter(models.Overtime.user_id==user_id)

#manager
def get_other_overtimes(db:Session, department: str, skip:int=0, limit: int=100):
    return db.query(models.Overtime).offset(skip).limit(limit).filter(models.Overtime.user_id.department==department)

def check_overtime(db:Session, overtime_id: int):
    db_overtime = db.query(models.Overtime).get(models.Overtime.id == overtime_id)
    db_overtime.update({"check":True})
    db.commit()
    return db_overtime

#hr
def all_overtimes(db:Session, skip: int=0, limit: int=100):
    return db.query(models.Overtime).offset(skip).limit(limit).filter(models.Overtime.check==True)