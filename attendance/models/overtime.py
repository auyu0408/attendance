from sqlalchemy import Column, ForeignKey, Integer, Date, String, Boolean, Time
from sqlalchemy.orm import relationship
import datetime

from attendance.database import Base

class Overtime(Base):
    __tablename__ = 'overtimes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    day = Column(Date, default=datetime.date.today)
    start = Column(Time)
    end = Column(Time)
    reason = Column(String)
    check = Column(Boolean, default=False)

    users = relationship("User", back_populates="overtimes")