from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from attendance.database import get_db
from attendance import schemas
from attendance.models import User
from attendance import crud
from attendance.dependency import get_current_user

router = APIRouter()
#hr
@router.get("/leave/{id}", response_model=schemas.Leave, status_code=200)
def hr_leave(id: int, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_leave(db, leave_id=id, current=current_user)

@router.get("/leave", response_model= List[schemas.Leave], status_code=200)
def hr_all_leave( db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.all_leave(db, current=current_user)