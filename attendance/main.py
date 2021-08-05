from attendance.models.user import User
from attendance.crud.user import authenticate_user, get_user_account
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from . import models, schemas
from .database import SessionLocal, engine
from attendance import crud

models.Base.metadata.create_all(bind= engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#authorized,token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm= Depends(), db:Session=Depends(get_db)):
    user_dict = crud.authenticate_user(db, account=form_data.username, passwd=form_data.password)
    if user_dict == "Wrong account":
        raise HTTPException(status_code=404, detail="Incorrect user account")
    if user_dict == "Wrong password.":
        raise HTTPException(status_code=400, detail="Wrong password.")
    return {"access_token": user_dict.account, "token_type": "bearer"}

async def get_current_user(token:str= Depends(oauth2_scheme), db:Session=Depends(get_db)):
    user = crud.get_user_account(db, user_account=token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},)
    return user

#USER
#self
@app.get("/profile/", response_model=schemas.User, status_code=200)
def get_self(current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return current_user

@app.put("/password/", status_code=204)
def change_passwd(password: schemas.UserPasswd, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.update_passwd(db, passwd=password, user_id=current_user.id)

#hr
@app.get("/hr/users/", response_model=List[schemas.User], status_code=200)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    if not current_user.hr:
        raise HTTPException(status_code=401, detail="Your are not hr.")
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/hr/users/{id}", response_model = schemas.User, status_code=200)
def get_user(id: int, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    if not current_user.hr:
        raise HTTPException(status_code=401, detail="Your are not hr.")
    db_user = crud.get_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return db_user

@app.post("/hr/users/", response_model = schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    if not current_user.hr:
        raise HTTPException(status_code=401, detail="Your are not hr.")
    db_user = crud.get_user_account(db, user_account=user.account)
    if db_user:
        raise HTTPException(status_code=400, detail="Account already exist.")
    return crud.create_user(db, user=user)

@app.put("/hr/users/{id}", response_model = schemas.User, status_code=200)
def update_user(user: schemas.User, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    if not current_user.hr:
        raise HTTPException(status_code=401, detail="Your are not hr.")
    db_user = crud.update_user(db, user=user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found.")
    return db_user

@app.delete("/hr/users/{id}", response_model = schemas.User, status_code=200)
def delete_user(id: int, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    if not current_user.hr:
        raise HTTPException(status_code=401, detail="Your are not hr.")
    db_user = crud.delete_user(db, user_id=id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User not found.")
    return db_user

#BASE_SALARY
#hr
@app.get("/hr/salary/{id}", response_model = List[schemas.BaseSalary], status_code=200)
def read_base_salary(id: int, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    if not current_user.hr:
        raise HTTPException(status_code=401, detail="Your are not hr.")
    return crud.get_base_salarys(db, user_id=id)

@app.post("/hr/salary/", status_code=201, response_model= List[schemas.BaseSalary])
def create_base_salary(salary: schemas.BaseSalaryCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    if not current_user.hr:
        raise HTTPException(status_code=401, detail="Your are not hr.")
    crud.create_salary(db, base_salary=salary)
    return crud.get_base_salarys(db, user_id=salary.user_id)

#LEAVE
#self
#@app.get("/leave/", response_model = List[schemas.Leave], status_code=200)

#@app.get("/leave_list/")