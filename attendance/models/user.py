from sqlalchemy import Boolean, Column, Integer, String, Date
from sqlalchemy.orm import relationship
import datetime

from attendance.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    account = Column(String(30), unique=True, index=True)
    passwd = Column(String)
    email = Column(String, unique=True, index=True)
    department = Column(String(20), index=True)
    manager = Column(Boolean, default=False)
    hr = Column(Boolean, default=False)
    on_job = Column(Date, default=datetime.date.today)
    off_job = Column(Date)
    status = Column(Integer, default=0)

    base_salarys = relationship("BaseSalary", back_populates="users")
    leaves = relationship("Leave", back_populates="users")
    overtimes = relationship("Overtime", back_populates="users")
    dailys = relationship("Daily", back_populates="users")