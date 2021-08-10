from pydantic import BaseModel
from enum import Enum
import datetime

class CategoryType(str, Enum):
    SICK = '病假'#0.5
    MENSTRUAL = '生理假'#0.5
    PERSONAL = '事假'#1
    TAKECARE = '家庭照顧假'#1
    NURSERY = '育嬰假'
    UNPAID = '無薪假'#1
    OTHER1 = '防疫隔離假'#1
    OTHER2 = '防疫照顧假'#1
    OTHER3 = '疫苗接種假'#1
    OTHER4 = '因公隔離'#0.5
    BUSINESS = '出差'
    OFFICIAL = '公假'
    INJURY = '公傷假'
    FUNERAL = '喪假'
    MARRIAGE = '婚假'
    MATERNITY = '產假'
    PATERNITY = '陪產假'
    PRENATAL = '產前假'
    ANNUAL = '特休'
    REST = '補休'


class LeaveCreate(BaseModel):
    start: datetime.datetime
    end: datetime.datetime
    category: CategoryType = CategoryType.PERSONAL
    reason: str

class Leave(LeaveCreate):
    id: int
    user_id: int
    check: bool

    class Config:
        orm_mode = True
