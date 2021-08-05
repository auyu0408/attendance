from sqlalchemy import Column, Integer, Date
import datetime

from attendance.database import Base

class DayOff(Base):
    __tablename__ = "day_offs"

    id = Column(Integer, primary_key=True)
    day = Column(Date, default= datetime.date.today)
    type = Column(Integer, default=6)