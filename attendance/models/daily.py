from typing import Optional
from pydantic import BaseModel
import datetime

class Daily(BaseModel):
    id: Optional[int]
    day: datetime.date
    on: datetime.time
    off:datetime.time
    on_fix: datetime.time
    off_fix: datetime.time
    fix_note: str