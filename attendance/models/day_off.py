from pydantic import BaseModel
import datetime

class DayOff(BaseModel):
    day: datetime.date
    type: str