from sqlalchemy.orm import Session
from fastapi import HTTPException
from attendance import models, schemas

#self
def get_dailys(db:Session, user_id: int):
    return db.query(models.Leave).filter(models.Leave.user_id==user_id)

#utility
def update_daily(db:Session, daily: schemas.DailyUpdate, daily_id: int, current: models.User):
    db_daily = db.query(models.Daily).get(models.Daily.id == daily_id)
    if db_daily.user_id != current.id and not current.hr:
        raise HTTPException(status_code=401, detail="Wrong User.")
    db_daily.on_fix= daily.on 
    db_daily.off_fix= daily.off
    db_daily.fix_note= daily.fix_note
    db.commit()
    db.refresh(db_daily)
    return db_daily

def get_daily(db:Session, id: int, current: models.User):
    db_daily = db.query(models.Leave).filter(models.Leave.id == id).first()
    if not db_daily:
        raise HTTPException(status_code=404, detail="Daily not found.")
    if db_daily.user_id != current.id and not current.hr:
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
    db_daily = models.Daily(day=daily.day, on=daily.on, off=daily.off, on_fix=daily.on, 
                    off_fix=daily.off, fix_note=daily.fix_note)
    db.add(db_daily)
    db.commit()
    db.refresh(db_daily)
    return db_daily
