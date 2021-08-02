from typing import Optional
from pydantic import BaseModel
import datetime

class Salary(BaseModel):
    id: Optional[int]
    user_id: rela
    date: datetime.date
    salary: int
    self_percent: int
    