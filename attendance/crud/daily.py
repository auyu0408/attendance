from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from fastapi import HTTPException
from attendance import models, schemas

#self
def get_dailys(db:Session, user_id: int):
    return db.query(models.Leave).filter(models.Leave.user_id == user_id)

#utility
def update_daily(db:Session, daily: schemas.DailyUpdate, id: int, current: models.User):
    db_daily = db.query(models.Daily).filter(models.Daily.id == id).first()
    if not db_daily:
        raise HTTPException(status_code=404, detail="Daily Not Found.")
    if db_daily.user_id != current.id and (not current.hr):
        raise HTTPException(status_code=401, detail="Wrong User.")
    db_daily.on_fix= daily.on_fix
    db_daily.off_fix= daily.off_fix
    db_daily.fix_note= daily.fix_note
    db.commit()
    db.refresh(db_daily)
    return db_daily

def get_daily(db:Session, id: int, current: models.User):
    db_daily = db.query(models.Daily).filter(models.Daily.id == id).first()
    if not db_daily:
        raise HTTPException(status_code=404, detail="Daily not found.")
    if db_daily.user_id != current.id:
        if not current.hr:
            raise HTTPException(status_code=401, detail="Wrong User.")
    return db_daily

#hr
def all_daily(db:Session, current: models.User, skip: int=0, limit: int=100):
    if not current.hr:
        raise HTTPException(status_code=401, detail="You are not hr.")
    return db.query(models.Daily).offset(skip).limit(limit).all()

def create_daily(db:Session, daily: schemas.DailyCreate, current: models.User):
    if not current.hr:
        raise HTTPException(status_code=401, detail="You are not hr.")
    user = db.query(models.User).filter(models.User.id==daily.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User_id not found.")
    if daily.on > daily.off:
        raise HTTPException(status_code=400, detail="Wrong time")
    db_daily = models.Daily(day=daily.day, on=daily.on, off=daily.off, on_fix=daily.on, 
                    off_fix=daily.off, fix_note=daily.fix_note, user_id=daily.user_id)
    db.add(db_daily)
    db.commit()
    db.refresh(db_daily)
    return db_daily
