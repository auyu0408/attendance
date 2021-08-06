from attendance.crud.leave import get_other_leaves
from attendance.crud.user import get_user
from attendance.models.leave import Leave
from sqlalchemy.sql.functions import current_date, current_user
from attendance.models.user import User
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from . import models, schemas
from .database import SessionLocal, engine
from attendance import crud
#from attendance.routers import base_salary

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
    return {"access_token": user_dict.account, "token_type": "bearer"}

async def get_current_user(token:str= Depends(oauth2_scheme), db:Session=Depends(get_db)):
    return crud.get_user_account(db, user_account=token)

#USER
#self
@app.get("/profile/", response_model=schemas.User, status_code=200)
def profile(current_user: User=Depends(get_current_user), db: Session=Depends(get_db)):
    return current_user

@app.put("/password/", status_code=204)
def change_passwd(password: schemas.UserPasswd, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.update_passwd(db, passwd=password, user_id=current_user.id)

#hr
@app.get("/hr/users/", response_model=List[schemas.User], status_code=200)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    if not current_user.hr:
        raise HTTPException(status_code=403, detail="Your are not hr.")
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/hr/users/{id}", response_model = schemas.User, status_code=200)
def read_user(id: int, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_user(db, user_id=id, current=current_user)

@app.post("/hr/users/", response_model = schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.create_user(db, user=user, current=current_user)

@app.put("/hr/users/{id}", response_model = schemas.User, status_code=200)
def update_user(user: schemas.User, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.update_user(db, user=user, current=current_user)

@app.delete("/hr/users/{id}", response_model = schemas.User, status_code=200)
def delete_user(id: int, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.delete_user(db, user_id=id, current=current_user)

#BASE_SALARY
#hr
@app.get("/hr/salary/{user_id}", response_model = List[schemas.BaseSalary], status_code=200)
def read_base_salary(user_id: int, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_base_salarys(db, user_id=id, current=current_user)

@app.post("/hr/salary/", status_code=201, response_model= List[schemas.BaseSalary])
def create_base_salary(salary: schemas.BaseSalaryCreate, db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    crud.create_salary(db, base_salary=salary, current=current_user)
    return crud.get_base_salarys(db, user_id=salary.user_id, current=current_user)

#LEAVE
#self
@app.get("/leave", response_model=List[schemas.Leave], status_code=200)
def leave_list(db: Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_leaves(db, user_id=current_user.id)

@app.get("/leave/{id}", response_model= schemas.Leave, status_code=200)
def read_leave(id: int, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_leave(db, leave_id=id, current=current_user)

@app.post("/leave", response_model=schemas.Leave, status_code=201)
def add_leave(leave_form: schemas.LeaveCreate, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.create_leave(db, Leave=leave_form, user_id=current_user.id)

@app.put("/leave", response_model=schemas.Leave, status_code=200)
def update_leave(leave_from: schemas.LeaveCreate, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.update_leave(db, Leave=leave_from, current=current_user)

@app.delete("/leave/{id}", response_model=schemas.Leave, status_code=200)
def delete_leave(id: int, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.delete_leave(db, leave_id=id, current=current_user)

#manager
@app.get("/check_leave", response_model=List[schemas.Leave], status_code=200)
def check_leave_list(db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_other_leaves(db, current=current_user)

@app.put("/check_leave/{id}", response_model=schemas.Leave, status_code=200)
def check_leave(id: int, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.check_leave(db, leave_id=id, current=current_user)

#hr
@app.get("/hr/leave/{id}", response_model=schemas.Leave, status_code=200)
def check_leave(id: int, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.get_leave(db, leave_id=id, current=current_user)

@app.get("/hr/leave/", response_model=schemas.Leave, status_code=200)
def check_leave(id: int, db: Session=Depends(get_db), current_user: User=Depends(get_current_user)):
    return crud.all_leave(db, current=current_user)