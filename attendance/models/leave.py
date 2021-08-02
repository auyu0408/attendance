from typing import Optional
from pydantic import BaseModel
import datetime

class Leave(BaseModel):
    id: Optional[int]
    start: datetime.datetime
    end: datetime.datetime
    category: str
    reason: str
    check: bool
