from attendance.database import Base
from pydantic import BaseModel
import datetime

class SalaryBase(BaseModel):
    salary: int

class SalaryCreate(SalaryBase):
    user_id: int
    date: datetime.date
    self_percent: int

class Salary(SalaryCreate):
    id: int
    
    class Config:
        orm_mode = True