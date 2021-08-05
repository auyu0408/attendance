from sqlalchemy import Column, ForeignKey, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relationship
import datetime

from attendance.database import Base

class Leave(Base):
    __tablename__ = 'leaves'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    start = Column(DateTime, default=datetime.datetime.now)
    end = Column(DateTime, default=datetime.datetime.now)
    category = Column(String)
    reason = Column(String)
    check = Column(Boolean, default=False)

    users = relationship("User", back_populates="leaves")