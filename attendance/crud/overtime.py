from attendance.schemas import user
from sqlalchemy.orm import Session
from attendance import dependency, models, schemas
from fastapi import HTTPException

#self
def create_overtime(db:Session, Overtime: schemas.OvertimeCreate, user_id: int):
    db_overtime = models.Overtime(day= Overtime.day, start= Overtime.start, end= Overtime.end, 
                        reason= Overtime.str, check= False, user_id = user_id)
    db.add(db_overtime)
    db.commit()
    db.refresh(db_overtime)
    return db_overtime

def update_overtime(db:Session, Overtime: schemas.OvertimeCreate, current: models.User, id: int):
    db_overtime = db.query(models.Overtime).filter(models.Overtime.id == id).first()
    if not db_overtime:
        raise HTTPException(status_code=404, detail="Overtime not found.")
    if current.id != db_overtime.user_id:
        raise HTTPException(status_code=401, detail="Wrong User.")
    db_overtime.day= Overtime.day
    db_overtime.start= Overtime.start
    db_overtime.end= Overtime.end
    db_overtime.reason= Overtime.reason
    db_overtime.check= False
    db.commit()
    return db_overtime

#utility
def get_overtime(db:Session, id: int, current: models.User):
    db_overtime = db.query(models.Overtime).filter(models.Overtime.id == id).first()
    if not db_overtime:
        raise HTTPException(status_code=404, detail="Overtime not found.")
    if db_overtime.user_id != current.id and not current.hr:
        raise HTTPException(status_code=401, detail="Wrong User.")

def get_overtimes(db:Session, user_id: int):
    return db.query(models.Overtime).filter(models.Overtime.user_id==user_id)

#manager
def get_other_overtimes(db:Session, current: models.User, skip:int=0, limit: int=100):
    if not current.manager:
        raise HTTPException(status_code=401, detail="You are not a manager.")
    if current.department == "Boss":
        return db.query(models.Overtime).offset(skip).limit(limit).filter(models.Overtime.user_id.manager==True)
    else:
        return db.query(models.Overtime).offset(skip).limit(limit).filter(models.Overtime.user_id.department==current.department)

def check_overtime(db:Session, overtime_id: int, current: models.User):
    if not current.manager:
        raise HTTPException(status_code=401, detail="You are not a manager.")
    db_overtime = db.query(models.Overtime).filter(models.Overtime.id == overtime_id).first()
    if not db_overtime:
        raise HTTPException(status_code=404, detail="Leave not found.")
    db_user = db.query(models.User).filter(models.User.id==db_overtime.user_id).first()
    if db_user.department != current.department:
        raise HTTPException(status_code=403, detail="Different Department.")
    if db_user.manager and current.department != "Boss":
        raise HTTPException(status_code=403, detail="Not enough limit.")
    db_overtime.check=True
    db.commit()
    return db_overtime

#hr
def all_overtime(db:Session, current: models.User, skip: int=0, limit: int=100):
    if not current.hr:
        raise HTTPException(status_code=401, detail="You are not hr.")
    return db.query(models.Overtime).offset(skip).limit(limit).filter(models.Overtime.check==True)