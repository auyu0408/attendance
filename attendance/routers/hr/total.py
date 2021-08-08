from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from attendance.database import get_db
from attendance import models
from attendance.dependency import get_current_user
import datetime

router = APIRouter()

@router.get("/total/{year}/{month}", status_code=200)
def total(year: int, month: int, db: Session=Depends(get_db), current: models.User=Depends(get_current_user)):
    if not current.hr:
        raise HTTPException(status_code=401, detail="You are not hr.")
    db_users = db.query(models.User).all()
    if month == 12:
        n_month = 1
        n_year = year+1
    else:
        n_month = month+1
        n_year = year
    db_leaves = db.query(models.Leave).filter(models.Leave.start>=datetime.datetime(year=year, month=month, day=1), models.Leave.end<datetime.datetime(year=n_year, month=n_month, day=1)).all()
    db_overtimes = db.query(models.Overtime).filter(models.Overtime.day>=datetime.datetime(year=year, month=month, day=1), models.Overtime.day<datetime.datetime(year=n_year, month=n_month, day=1)).all()
    db_dailys = db.query(models.Daily).filter(models.Daily.day>=datetime.datetime(year=year, month=month, day=1), models.Daily.day<datetime.datetime(year=n_year, month=n_month, day=1)).all()
    db_dayoffs = db.query(models.DayOff).filter(models.DayOff.day>=datetime.datetime(year=year, month=month, day=1), models.DayOff.day<datetime.datetime(year=n_year, month=n_month, day=1)).all()
    result = {"users": db_users, "leaves": db_leaves, "overtimes": db_overtimes, "dailys": db_dailys, "dayoffs": db_dayoffs}
    return result
