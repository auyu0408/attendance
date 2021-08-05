from sqlalchemy.orm import Session
from attendance import models, schemas
#hr
def get_dayoff(db:Session, date_id: int):
    return db.query(models.DayOff).filter(models.DayOff.id == date_id).first()

def all_dayoff(db:Session, skip: int=0, limit: int=100):
    return db.query(models.DayOff).offset(skip).limit(limit).all()

def create_dayoff(db:Session, date:schemas.DayOff):
    db_dayoff = models.DayOff(
        day = date.day,
        type = date.type)
    db.add(db_dayoff)
    db.commit()
    db.refresh(db_dayoff)
    return db_dayoff

def delete_dayoff(db:Session, date_id: int):
    db_dayoff = db.query(models.DayOff).get(models.DayOff.id == date_id)
    if db_dayoff:
        db.delete(db_dayoff)
        db.commit()
    return all_dayoff
