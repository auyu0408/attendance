from attendance.models.user import User
from salalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
import datetime 

#hash passwd
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def authenticate_user(db:Session, Login: schemas.UserLogin):
    try:
        user = db.query(models.User).filter(models.User.account == Login).first()
    except:
        return "Wrong account"
    if pwd_context.verify(Login.passwd, user.passwd):
        return User
    else:
        return "Wrong password."    

def get_user(db:Session, user_id: int):
    return db.query(models.User).filter(models.User.id==user_id).first()

def update_passwd(db:Session, passwd: schemas.UserPasswd, user_id: int):
    try:
        db_user = db.query(models.User).get(models.User.id==user_id)
    except:
        return False
    if pwd_context.verify(passwd.origin, db_user.passed):
        hash_new = pwd_context.hash(passwd.new)
        db_user.update({
            "passwd": hash_new
        })
        db.commit()
        return True
    else:
        return False

#hr
def get_users(db: Session, skip: int=0, limit: int=100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db:Session, user:schemas.UserCreate):
    hash_passwd = pwd_context.hash(user.passwd)
    db_user = models.User(name=user.name, account=user.account, email=user.email, passwd=hash_passwd,
            department = user.department, manager = user.manager, hr = user.hr, on_job = user.on_job, off_job=user.off_job
            , status=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db:Session, user_id: int):
    db_user = db.query(models.User).get(models.User.id==user_id)
    db_user.update({
        "status": 2,
        "off_job": datetime.date.today()
        })
    db.commit()
    return db_user

def update_user(db:Session, user: schemas.User):
    db_user = db.query(models.User).get(models.User.id == user.id)
    db_user.update({
        "name": user.name,
        "account": user.account,
        "email": user.email,
        "department": user.department,
        "manager": user.manager,
        "hr": user.hr,
        "on_job": user.on_job,
        "off_job": user.off_job,
        "status": user.status,
    })
    db.commit()
    db.refresh(db_user)
    return db_user