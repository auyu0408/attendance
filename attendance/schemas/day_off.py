from pydantic import BaseModel
import datetime

class DayOffCreate(BaseModel):
    day: datetime.date
    type: int

class DayOff(DayOffCreate):
    id: int

    class Config:
        orm_model = True