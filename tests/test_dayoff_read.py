from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.orm import Session

from attendance.main import app, login
from attendance import crud
from attendance.database import get_db

client = TestClient(app)

async def override_dependency(form_data: OAuth2PasswordRequestForm= Depends(), db:Session=Depends(get_db)):
    user_dict = crud.authenticate_user(db, account=form_data.username, passwd=form_data.password)
    return {"access_token": user_dict.account, "token_type": "bearer"}

app.dependency_overrides[login] = override_dependency

admin = {"accept": "application/json", "Authorization": "Bearer boss1", "Content-Type": "application/json"}
officer = {"accept": "application/json", "Authorization": "Bearer officer1", "Content-Type": "application/json"}

def test_dayoff_get_success():
    response = client.get("/hr/day_off/1", headers=admin)
    assert response.status_code == 200
    print(response.json())

def test_dayoff_gets():
    response = client.get("/hr/day_off", headers=admin)
    assert response.status_code == 200
    print(response.json())

def test_dayoff_get_staff():
    response = client.get("/hr/day_off/3", headers=officer)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You are not hr."
    }

def test_dayoff_gets_staff():
    response = client.get("/hr/day_off", headers=officer)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You are not hr."
    }

def test_dayoff_get_notfound():
    response = client.get("/hr/day_off/20", headers=admin)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "DayOff not found."
    }