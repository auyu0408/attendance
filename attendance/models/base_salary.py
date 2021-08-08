from sqlalchemy import Column, ForeignKey, Integer, Date
from sqlalchemy.orm import relationship
import datetime

from attendance.database import Base

class BaseSalary(Base):
    __tablename__ = 'base_salarys'

    id = Column(Integer, primary_key=True, index= True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, default=datetime.date.today)
    salary = Column(Integer, default=0)
    self_percent = Column(Integer, default=0)

    users = relationship("User", back_populates="base_salarys")