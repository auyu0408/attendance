from attendance.models.salary import Salary
from typing import Optional
from pydantic import BaseModel
import datetime

class User(BaseModel):
    id: Optional[int]
    name: str
    account: str
    passwd: str
    email: str
    department: str
    manager: bool
    hr: bool
    on_job: datetime.date
    off_job: datetime.date

    children: List[Salary] = []