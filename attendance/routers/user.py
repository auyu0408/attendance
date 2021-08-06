from typing import List

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from attendance import models, schemas
from attendance import crud
from fastapi import APIRouter

user_router = APIRouter()

#USER
#self
@user_router.get("/profile/", response_model=schemas.User, status_code=200)
def get_self(current_user: models.User=Depends()):
    return current_user

@user_router.put("/password/", status_code=204)
def change_passwd(password: schemas.UserPasswd, db: Session=Depends(), current_user: models.User=Depends()):
    return crud.update_passwd(db, passwd=password, user_id=current_user.id)

#hr
@user_router.get("/hr/users/", response_model=List[schemas.User], status_code=200)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends()):
    #if not current_user.hr:
    #    raise HTTPException(status_code=401, detail="Your are not hr.")
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@user_router.get("/hr/users/{id}", response_model = schemas.User, status_code=200)
def get_user(id: int, db: Session = Depends(), current_user: models.User=Depends()):
    if not current_user.hr:
        raise HTTPException(status_code=401, detail="Your are not hr.")
    db_user = crud.get_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return db_user

@user_router.post("/hr/users/", response_model = schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends()):
    #if not current_user.hr:
    #    raise HTTPException(status_code=401, detail="Your are not hr.")
    db_user = crud.get_user_account(db, user_account=user.account)
    if db_user:
        raise HTTPException(status_code=400, detail="Account already exist.")
    return crud.create_user(db, user=user)

@user_router.put("/hr/users/{id}", response_model = schemas.User, status_code=200)
def update_user(user: schemas.User, db: Session = Depends(), current_user: models.User=Depends()):
    if not current_user.hr:
        raise HTTPException(status_code=401, detail="Your are not hr.")
    db_user = crud.update_user(db, user=user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found.")
    return db_user

@user_router.delete("/hr/users/{id}", response_model = schemas.User, status_code=200)
def delete_user(id: int, db: Session = Depends(), current_user: models.User=Depends()):
    if not current_user.hr:
        raise HTTPException(status_code=401, detail="Your are not hr.")
    db_user = crud.delete_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found.")
    return db_user