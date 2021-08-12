from datetime import datetime
from sqlalchemy.orm import Session
from attendance import models, schemas
from fastapi import HTTPException
import datetime

#self
def create_overtime(db:Session, Overtime: schemas.OvertimeCreate, user_id: int):
    dayoff = db.query(models.DayOff).filter(models.DayOff.day == Overtime.day).first()
    if dayoff:
        if Overtime.start == datetime.time(8,0) or Overtime.start == datetime.time(13,0):
            pass
        else:
            raise HTTPException(status_code=400, detail="Wrong start time.")
    else:
        if Overtime.start == datetime.time(17,30):
            pass
        else:
            raise HTTPException(status_code=400, detail="Wrong start time.")
    if Overtime.start > Overtime.end:
        raise HTTPException(status_code=400, detail="Wrong time.")
    db_overtime = models.Overtime(day= Overtime.day, start= Overtime.start, end= Overtime.end, 
                        reason= Overtime.reason, check= False, user_id = user_id)
    db.add(db_overtime)
    db.commit()
    db.refresh(db_overtime)
    return db_overtime

def update_overtime(db:Session, Overtime: schemas.OvertimeCreate, current: models.User, id: int):
    dayoff = db.query(models.DayOff).filter(models.DayOff.day == Overtime.day).first()
    if dayoff:
        if Overtime.start == datetime.time(8,0) or Overtime.start == datetime.time(13,0):
            pass
        else:
            raise HTTPException(status_code=400, detail="Wrong start time.")
    else:
        if Overtime.start == datetime.time(17,30):
            pass
        else:
            raise HTTPException(status_code=400, detail="Wrong start time.")
    if Overtime.start > Overtime.end:
        raise HTTPException(status_code=400, detail="Wrong time.")
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

def get_overtime(db:Session, id: int, current: models.User):
    db_overtime = db.query(models.Overtime).filter(models.Overtime.id == id).first()
    if not db_overtime:
        raise HTTPException(status_code=404, detail="Overtime not found.")
    if db_overtime.user_id != current.id:
        raise HTTPException(status_code=401, detail="Wrong User.")
    return db_overtime

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

def get_overtime_manager(db:Session, id: int, current: models.User):
    if not current.manager:
        raise HTTPException(status_code=401, detail="You are not a manager.")
    db_overtime = db.query(models.Overtime).filter(models.Overtime.id == id).first()
    if not db_overtime:
        raise HTTPException(status_code=404, detail="Overtime not found.")
    db_user = db.query(models.User).filter(models.User.id == db_overtime.user_id)
    if db_user.department != current.department:
        if db_user.manager == True and current.department == "Boss":
            pass
        else: 
            raise HTTPException(status_code=401, detail="Different department.")
    else:
        if db_user.department != "Boss" and db_user.manager == True:
            raise HTTPException(status_code=401, detail="You can't check the leave by yourselves.")
    return db_overtime

def check_overtime(db:Session, overtime_id: int, current: models.User):
    if not current.manager:
        raise HTTPException(status_code=401, detail="You are not a manager.")
    db_overtime = db.query(models.Overtime).filter(models.Overtime.id == overtime_id).first()
    if not db_overtime:
        raise HTTPException(status_code=404, detail="Leave not found.")
    db_user = db.query(models.User).filter(models.User.id==db_overtime.user_id).first()
    if db_user.department != current.department:
        if db_user.manager == True and current.department == "Boss":
            pass
        else:
            raise HTTPException(status_code=401, detail="Different Department.")
    if db_user.department != "Boss" and db_user.manager == True:
        raise HTTPException(status_code=401, detail="You can't check the leave by yourselves.")
    db_overtime.check=True
    db.commit()
    return db_overtime

#hr
def all_overtime(db:Session, current: models.User, skip: int=0, limit: int=100):
    if not current.hr:
        raise HTTPException(status_code=401, detail="You are not hr.")
    return db.query(models.Overtime).offset(skip).limit(limit).filter(models.Overtime.check==True)

def get_overtime_hr(db:Session, id: int, current: models.User):
    if not current.hr:
        raise HTTPException(status_code=401, detail="You are not hr.")
    db_overtime = db.query(models.Overtime).filter(models.Overtime.id == id, models.Overtime.check == True).first()
    if not db_overtime:
        raise HTTPException(status_code=404, detail="Overtime not found.")
    return db_overtime