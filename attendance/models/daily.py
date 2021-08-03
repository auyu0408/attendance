from sqlalchemy import Column, ForeignKey, Integer, Date, String, Time
from sqlalchemy.orm import relationship
import datetime

from attendance.database import Base

class Daily(Base):
    __tablename__ = 'dailys'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    day =Column(Date, default=datetime.date.today)
    on = Column(Time, default=datetime.datetime.now.time)
    off = Column(Time, default=datetime.datetime.now.time)
    on_fix = Column(Time, default=datetime.datetime.now.time)
    off_fix = Column(Time, default=datetime.datetime.now.time)
    fix_note = Column(String)

    users = relationship("User", back_populates="dailys")