from sqlalchemy.orm import Session
from fastapi import HTTPException, Response

from attendance import models, schemas
#hr
def get_dayoff(db:Session, date_id: int, current: models.User):
    if not current.hr:
        raise HTTPException(status_code=401, detail="You are not hr.")
    db_dayoff = db.query(models.DayOff).filter(models.DayOff.id == date_id).first()
    if not db_dayoff:
        raise HTTPException(status_code=404, detail="DayOff not found.")
    return db_dayoff

def all_dayoff(db:Session, current: models.User, skip: int=0, limit: int=100):
    if not current.hr:
        raise HTTPException(status_code=401, detail="You are not hr.")
    db_dayoffs = db.query(models.DayOff).offset(skip).limit(limit).all()
    return db_dayoffs

def create_dayoff(db:Session, date:schemas.DayOffCreate, current: models.User):
    if not current.hr:
        raise HTTPException(status_code=401, detail="You are not hr.")
    dayoff = db.query(models.DayOff).filter(models.DayOff.day == date.day).first()
    if dayoff:
        raise HTTPException(status_code=400, detail="Reapeat day.")
    db_dayoff = models.DayOff(day = date.day, type = date.type)
    db.add(db_dayoff)
    db.commit()
    db.refresh(db_dayoff)
    return db_dayoff

def delete_dayoff(db:Session, date_id: int, current: models.User):
    if not current.hr:
        raise HTTPException(status_code=401, detail="You are not hr.")
    db_dayoff = db.query(models.DayOff).filter(models.DayOff.id == date_id).first()
    if db_dayoff:
        db.delete(db_dayoff)
        db.commit()
    else: 
        raise HTTPException(status_code=404, detail="Object not found")
    return Response(status_code=204)
