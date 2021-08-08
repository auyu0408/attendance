import datetime
from attendance.crud import overtime
from fastapi import Depends, FastAPI, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from . import models
from .database import get_db, engine
from attendance import crud
from attendance.routers import user, leave, overtime, daily, hr

models.Base.metadata.create_all(bind= engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

@app.post("/get_init_user")
def admin(db: Session=Depends(get_db)):
    db_admin = db.query(models.User).first()
    if not db_admin:
        hash_passwd = pwd_context.hash("admin")
        db_admin = models.User(name="admin", account="admin", email="admin@gmail.com", passwd=hash_passwd,
            department = "admin", manager = True, hr = True, on_job = datetime.date.today(), off_job=datetime.date.today()
            , status=0)
        db.add(db_admin)
        db.commit()
        return Response(status_code=201)
    else: return Response(status_code=204)


def get_form():
    return {"username": "admin", "password": "admin"}

#Dependency
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm= Depends(), db:Session=Depends(get_db)):
    user_dict = crud.authenticate_user(db, account=form_data.username, passwd=form_data.password)
    return {"access_token": user_dict.account, "token_type": "bearer"}

#router
app.include_router(user.router)
app.include_router(leave.router)
app.include_router(overtime.router)
app.include_router(daily.router)

app.include_router(hr.user.router, prefix="/hr")
app.include_router(hr.base_salary.router, prefix="/hr")
app.include_router(hr.leave.router, prefix="/hr")
app.include_router(hr.overtime.router, prefix="/hr")
app.include_router(hr.daily.router, prefix="/hr")
app.include_router(hr.day_off.router, prefix="/hr")
app.include_router(hr.total.router, prefix="/hr")