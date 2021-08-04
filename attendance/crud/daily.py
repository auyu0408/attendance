from salalchemy.orm import Session
from . import models, schemas

def get_daily(db:Session, id: int):
    return db.query(models.Leave).filter(models.Leave.id == id).first()

def get_dailys(db:Session, user_id: int):
    return db.query(models.Leave).filter(models.Leave.user_id==user_id)

#utility
def update_daily(db:Session, daily: schemas.DailyUpdate, daily_id: int):
    db_daily = db.query(models.Daily).get(models.Daily.id == daily_id)
    db_daily.update({
        "on_fix": daily.on, 
        "off_fix": daily.off,
        "fix_note": daily.fix_note})
    db.commit()
    db.refresh(db_daily)
    return db_daily

#hr
def all_daily(db:Session, skip: int=0, limit: int=100):
    return db.query(models.Daily).offset(skip).limit(limit).all()

def create_daily(db:Session, daily: schemas.DailyCreate):
    db_daily = models.Daily(day=daily.day, on=daily.on, off=daily.off, on_fix=daily.on, 
                    off_fix=daily.off, fix_note=daily.fix_note)
    db.add(db_daily)
    db.commit()
    db.refresh(db_daily)
    return db_daily
