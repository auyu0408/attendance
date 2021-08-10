from attendance.crud import overtime
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from . import models
from .database import get_db, engine
from attendance import crud
from attendance.routers import user, leave, overtime, daily, hr

models.Base.metadata.create_all(bind= engine)

app = FastAPI()

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