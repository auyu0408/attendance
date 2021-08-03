from pydantic import BaseModel
import datetime

class UserBase(BaseModel):
    account: str

class UserLogin(UserBase):
    passwd: str

class UserCreate(UserLogin):
    name: str
    email: str
    department: str
    manager: bool
    hr: bool
    on_job: datetime.date
    off_job: datetime.date
    status: int

class User(UserBase):
    id: int
    name: str
    email: str
    department: str
    manager: bool
    hr: bool
    on_job: datetime.date
    off_job: datetime.date
    status: int

    class Config:
        orm_mode = True