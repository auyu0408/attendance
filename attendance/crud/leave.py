from sqlalchemy.orm import Session
from attendance import models, schemas

#self
def delete_leave(db:Session, leave_id: int):
    db_leave = db.query(models.Leave).get(models.Leave.id == leave_id)
    db.delete(db_leave)
    db.commit
    return get_leaves

def create_leave(db:Session, Leave: schemas.LeaveCreate, user_id: int):
    db_leave = models.Leave(start= Leave.start, end= Leave.end, category= Leave.category,
                        reason= Leave.str, check= False, user_id = user_id)
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave

def update_leave(db:Session, Leave: schemas.LeaveCreate):
    db_leave = db.query(models.Leave).filter(models.Leave.id == Leave.id)
    db_leave.update({
        "start": Leave.start, 
        "end": Leave.end,
        "category": Leave.category, 
        "reason": Leave.reason,
        "check": False
    })
    db.commit()
    return db_leave

#utility
def get_leave(db:Session, leave_id: int):
    return db.query(models.Leave).filter(models.Leave.id == leave_id).first()

def get_leaves(db:Session, user_id: int):
    return db.query(models.Leave).filter(models.Leave.user_id==user_id)

#manager
def get_other_leaves(db:Session, department: str, skip:int=0, limit: int=100):
    return db.query(models.Leave).offset(skip).limit(limit).filter(models.Leave.user_id.department==department)

def check_leave(db:Session, leave_id: int):
    db_leave = db.query(models.Leave).get(models.Leave.id == leave_id)
    db_leave.update({"check":True})
    db.commit()
    return db_leave

#hr
def all_leave(db:Session, skip: int=0, limit: int=100):
    return db.query(models.Leave).offset(skip).limit(limit).filter(models.Leave.check==True)