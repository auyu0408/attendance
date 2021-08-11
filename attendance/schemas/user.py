from pydantic import BaseModel
import datetime
from enum import Enum

class StatusType(int, Enum):
    ON_JOB = 0
    UNPAID = 1
    OFF_JOB = 2

class UserBase(BaseModel):
    account: str

class UserLogin(UserBase):
    passwd: str

class UserPasswd(BaseModel):
    origin: str
    new: str

class UserCreate(UserLogin):
    name: str
    email: str
    department: str
    manager: bool
    hr: bool
    on_job: datetime.date
    off_job: datetime.date

class UserUpdate(UserBase):
    name: str
    email: str
    department: str
    manager: bool
    hr: bool
    on_job: datetime.date
    status: StatusType = StatusType.ON_JOB

class User(UserUpdate):
    id: int
    off_job: datetime.date
    class Config:
        orm_mode = True