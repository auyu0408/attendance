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

officer = {"accept": "application/json", "Authorization": "Bearer officer1", "Content-Type": "application/json"}
admin = {"accept": "application/json", "Authorization": "Bearer admin", "Content-Type": "application/json"}
manager = {"accept": "application/json", "Authorization": "Bearer manager1", "Content-Type": "application/json"}

def test_get_daily_admin():
    response = client.get("/hr/daily/1", headers=admin)
    assert response.status_code == 200
    print(response.json())

def test_get_daily_officer():
    response = client.get("/daily/1", headers=officer)
    assert response.status_code == 200
    print(response.json())

def test_gets_daily_admin():
    response = client.get("/hr/daily", headers=admin)
    assert response.status_code == 200
    print(response.json())

def test_gets_daily_officer_hr():
    response = client.get("/hr/daily", headers=officer)
    assert response.status_code == 401
    assert response.json() == {
        "detail" : "You are not hr."
    }

def test_get_daily_notfound():
    response = client.get("/hr/daily/20", headers=admin)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Daily not found."
    }

def test_get_daily_notfound_staff():
    response = client.get("/hr/daily/23", headers=officer)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Daily not found."
    }   

def test_get_daily_manager():
    response = client.get("/daily/2", headers=manager)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Wrong User."
    }

def test_gets_daily_manager():
    response = client.get("/hr/daily", headers=manager)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You are not hr."
    }