from pydantic import BaseModel
import datetime

class DailyCreate(BaseModel):
    day: datetime.date
    on: datetime.time
    off:datetime.time
    on_fix: datetime.time
    off_fix: datetime.time
    fix_note: str

class Daily(DailyCreate):
    id: int

    class Config:
        orm_mode = True