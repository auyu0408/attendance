from attendance.database import Base
from pydantic import BaseModel
import datetime

class SalaryCreate(BaseModel):
    salary: int
    user_id: int
    date: datetime.date
    self_percent: int

class Salary(SalaryCreate):
    id: int
    
    class Config:
        orm_mode = True