from sqlalchemy.sql.operators import startswith_op
from pydantic import BaseModel
import datetime

class OvertimeCreate(BaseModel):
    day: datetime.date
    start: datetime.time
    end: datetime.time
    reason: str
    check: bool

class Overtime(OvertimeCreate):
    id: int

    class Config:
        orm_mode = True