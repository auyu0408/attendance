from pydantic import BaseModel
import datetime

class DailyUpdate(BaseModel):
    on_fix: datetime.time
    off_fix: datetime.time
    fix_note: str

class DailyCreate(DailyUpdate):
    user_id: int
    day: datetime.date
    on: datetime.time
    off: datetime.time

class Daily(DailyCreate):
    id: int

    class Config:
        orm_mode = True