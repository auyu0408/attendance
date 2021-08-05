from pydantic import BaseModel
import datetime

class LeaveCreate(BaseModel):
    start: datetime.datetime
    end: datetime.datetime
    category: str
    reason: str
    check: bool

class Leave(LeaveCreate):
    id: int

    class Config:
        orm_mode = True
