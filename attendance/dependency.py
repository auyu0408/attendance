from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.orm import Session

from attendance import crud
from attendance.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token:str= Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return crud.get_user_account(db, user_account=token)