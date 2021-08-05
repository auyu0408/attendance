from pydantic import BaseModel
from typing import Optional
import datetime

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

class User(UserBase):
    id: int
    name: str
    email: str
    department: str
    manager: bool = False
    hr: bool = False
    on_job: datetime.date
    off_job: Optional[datetime.date]
    status: int = 0

    class Config:
        orm_mode = True