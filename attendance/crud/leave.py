from sqlalchemy.orm import Session
from attendance import database, models, schemas
from fastapi import HTTPException

#self
def delete_leave(db:Session, leave_id: int, current: models.User):
    db_leave = db.query(models.Leave).filter(models.Leave.id == leave_id).first()
    if not db_leave:
        raise HTTPException(status_code=404, detail="Leave not found.")
    if db_leave.id != current.id:
        raise HTTPException(status_code=401, detail="Wrong user.")
    db.delete(db_leave)
    db.commit
    return get_leaves(db, user_id=current.id)

def create_leave(db:Session, Leave: schemas.LeaveCreate, user_id: int):
    db_leave = models.Leave(start= Leave.start, end= Leave.end, category= Leave.category,
                        reason= Leave.str, check= False, user_id = user_id)
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave

def update_leave(db:Session, Leave: schemas.LeaveCreate, current: models.User):
    db_leave = db.query(models.Leave).filter(models.Leave.id == Leave.id).first()
    if not db_leave:
        raise HTTPException(status_code=404, detail="not_found")
    if db_leave.user_id != current.id:
        raise HTTPException(status_code=401, detail="Wrong User.")
    db_leave.start= Leave.start
    db_leave.end= Leave.end
    db_leave.category= Leave.category
    db_leave.reason= Leave.reason
    db_leave.check= False
    db.commit()
    return db_leave

#utility
def get_leave(db:Session, leave_id: int, current: models.User):
    leave = db.query(models.Leave).filter(models.Leave.id == leave_id).first()
    if not leave:
        raise HTTPException(status_code=404, detail="not found.")
    if leave.user_id != current.id and not current.hr:
        raise HTTPException(status_code=401, detail="Wrong user.")
    return leave

def get_leaves(db:Session, user_id: int):
    return db.query(models.Leave).filter(models.Leave.user_id==user_id)

#manager
def get_other_leaves(db:Session, current: models.User, skip:int=0, limit: int=100):
    if not current.manager:
        raise HTTPException(status_code=401, detail="You are not a manager.")
    if current.department == "Boss":
        return db.query(models.Leave).offset(skip).limit(limit).filter(models.Leave.user_id.manager==True)
    else:
        return db.query(models.Leave).offset(skip).limit(limit).filter(models.Leave.user_id.department==current.department)

def check_leave(db:Session, leave_id: int, current: models.User):
    if not current.manager:
        raise HTTPException(status_code=401, detail="You are not a manager.")
    db_leave = db.query(models.Leave).filter(models.Leave.id == leave_id).first()
    if not db_leave:
        raise HTTPException(status_code=404, detail="Leave not found.")
    db_user = db.query(models.User).filter(models.User.id==db_leave.user_id).first()
    if db_user.department != current.department:
        raise HTTPException(status_code=403, detail="Different Department.")
    if db_user.manager and current.department != "Boss":
        raise HTTPException(status_code=403, detail="Not enough limit.")
    db_leave.check=True
    db.commit()
    return db_leave

#hr
def all_leave(db:Session, current: models.User, skip: int=0, limit: int=100):
    if not current.hr:
        raise HTTPException(status_code=401, detail="You are not hr.")
    return db.query(models.Leave).offset(skip).limit(limit).filter(models.Leave.check==True)