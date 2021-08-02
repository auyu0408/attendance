from typing import Optional
from pydantic import BaseModel
import datetime

class Overtime(BaseModel):
    id: Optional[int]
    day: datetime.date
    start: datetime.time
    end: datetime.time
    reason: str
    check: bool