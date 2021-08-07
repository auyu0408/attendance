from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from attendance.database import get_db
from attendance import schemas
from attendance.models import User
from attendance import crud
from attendance.dependency import get_current_user

router = APIRouter()

#USER
#self
@router.get("/profile/", response_model=schemas.User, status_code=200)
def profile(current_user: User=Depends(get_current_user)):
    return current_user

@router.put("/password/", status_code=204)
def change_passwd(password: schemas.UserPasswd, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.update_passwd(db, passwd=password, user_id=current_user.id)