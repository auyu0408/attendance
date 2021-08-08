from sqlalchemy.orm import Session
from attendance import models, schemas
from passlib.context import CryptContext
from fastapi import HTTPException
import datetime 

#hash passwd
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(db:Session, account: str, passwd:str):
    user = db.query(models.User).filter(models.User.account == account).first()
    if not user:
        raise HTTPException(status_code=404, detail="Incorrect user account")
    if pwd_context.verify(passwd, user.passwd):
        return user
    else:
        raise HTTPException(status_code=400, detail="Wrong password.")  

def get_user(db:Session, user_id: int, current: models.User):
    if not current.hr:
        raise HTTPException(status_code=401, detail="You are not a hr.")
    db_user = db.query(models.User).filter(models.User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    return db_user

def get_user_account(db:Session, user_account: str):
    db_user = db.query(models.User).filter(models.User.account==user_account).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},)
    return db_user

def update_passwd(db:Session, passwd: schemas.UserPasswd, user_id: int):
    db_user = db.query(models.User).filter(models.User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if pwd_context.verify(passwd.origin, db_user.passwd):
        hash_new = pwd_context.hash(passwd.new)
        db_user.passwd = hash_new
        db.commit()
        return True
    else:
        raise HTTPException(status_code=400, detail="Wrong password.")

#hr
def get_users(db: Session, current: models.User, skip: int=0, limit: int=100):
    if not current.hr:
        raise HTTPException(status_code=401, detail="You are not hr.")
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db:Session, user:schemas.UserCreate, current: models.User):
    if not current.hr:
        raise HTTPException(status_code=401, detail="Your are not hr.")
    hash_passwd = pwd_context.hash(user.passwd)
    already_user = db.query(models.User).filter(models.User.account==user.account).first()
    if already_user:
        raise HTTPException(status_code=400, detail="Account already exist.")
    db_user = models.User(name=user.name, account=user.account, email=user.email, passwd=hash_passwd,
            department = user.department, manager = user.manager, hr = user.hr, on_job = user.on_job, off_job=user.off_job
            , status=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db:Session, user_id: int, current: models.User):
    if not current.hr:
        raise HTTPException(status_code=401, detail="Your are not hr.")
    db_user = db.query(models.User).filter(models.User.id==user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    else:
        db_user.status= 2,
        db_user.off_job= datetime.date.today()
        db.commit()
    return db_user

def update_user(db:Session, user: schemas.User, current: models.User):
    if not current.hr:
        raise HTTPException(status_code=401, detail="Your are not hr.")
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")
    else:
        db_user.name= user.name
        db_user.account= user.account
        db_user.email= user.email
        db_user.department= user.department
        db_user.manager= user.manager
        db_user.hr= user.hr
        db_user.on_job= user.on_job
        db_user.off_job= user.off_job
        db_user.status= user.status
        db.commit()
        db.refresh(db_user)
    return db_user