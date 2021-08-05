from sqlalchemy.sql.operators import startswith_op
from pydantic import BaseModel
import datetime

class OvertimeCreate(BaseModel):
    day: datetime.date
    start: datetime.time
    end: datetime.time
    reason: str

class Overtime(OvertimeCreate):
    id: int
    check: bool
    user_id: int

    class Config:
        orm_mode = True