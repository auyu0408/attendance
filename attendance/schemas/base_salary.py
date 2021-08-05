from pydantic import BaseModel
import datetime

class BaseSalaryCreate(BaseModel):
    salary: int
    user_id: int
    date: datetime.date
    self_percent: int

class BaseSalary(BaseSalaryCreate):
    id: int
    
    class Config:
        orm_mode = True