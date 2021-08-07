from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from attendance.database import get_db
from attendance import schemas
from attendance.models import User
from attendance import crud
from attendance.dependency import get_current_user

router = APIRouter()

#USER
#hr
@router.get("/users", response_model=List[schemas.User], status_code=200)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_users(db, current=current_user, skip=skip, limit=limit)

@router.get("/users/{id}", response_model = schemas.User, status_code=200)
def read_user(id: int, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_user(db, user_id=id, current=current_user)

@router.post("/users", response_model = schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.create_user(db, user=user, current=current_user)

@router.put("/users/{id}", response_model = schemas.User, status_code=200)
def update_user(user: schemas.User, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.update_user(db, user=user, current=current_user)

@router.delete("/users/{id}", response_model = schemas.User, status_code=200)
def delete_user(id: int, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.delete_user(db, user_id=id, current=current_user)