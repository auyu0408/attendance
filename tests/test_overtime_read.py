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
manager = {"accept": "application/json", "Authorization": "Bearer manager1", "Content-Type": "application/json"}
hr = {"accept": "application/json", "Authorization": "Bearer hr1", "Content-Type": "application/json"}
hr_manager = {"accept": "application/json", "Authorization": "Bearer hrmanager1", "Content-Type": "application/json"}
boss = {"accept": "application/json", "Authorization": "Bearer boss1", "Content-Type": "application/json"}
#usually
def test_get_overtimes_officer():
    response = client.get("/overtime", headers=officer)
    print(response.json())
    assert response.status_code == 200

def test_get_overtimes_manager():
    response = client.get("/overtime", headers=manager)
    print(response.json())
    assert response.status_code == 200

def test_get_overtime_officer():
    response = client.get("/overtime/1", headers=officer)
    assert response.status_code == 200

def test_get_overtime_manager():
    response = client.get("/overtime/1", headers=manager)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Wrong User."
    }

def test_get_overtime_notfound():
    response = client.get("/overtime/20", headers=manager)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Overtime not found."
    }

#check manager
def test_check_overtimes_manager():
    response = client.get("/check_overtime", headers=manager)
    print(response.json())
    assert response.status_code == 200

def test_check_overtime_manager():
    response = client.get("/check_overtime/1", headers=manager)
    print(response.json())
    assert response.status_code == 200

def test_check_overtime_notfound():
    response = client.get("/check_overtime/20", headers=manager)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Permission denied."
    }

def test_check_overtime_hr():
    response = client.get("/check_overtime/3", headers=manager)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Permission denied."
    }

def test_check_overtime_self():
    response = client.get("/check_overtime/2", headers=manager)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Permission denied."
    }

#check officer
def test_check_overtimes_officer():
    response = client.get("/check_overtime", headers=officer)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You are not a manager."
    }

def test_check_overtime_officer():
    response = client.get("/check_overtime/1", headers=officer)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You are not a manager."
    }

#check boss
def test_check_overtimes_boss():
    response = client.get("/check_overtime", headers=boss)
    assert response.status_code == 200
    print(response.json())

def test_check_overtime_boss():
    response = client.get("/check_overtime/2", headers=boss)
    assert response.status_code == 200
    print(response.json())

def test_check_overtime_bossself():
    response = client.get("/check_overtime/5", headers=boss)
    assert response.status_code == 200
    print(response.json())

def test_check_overtime_boss_staff():
    response = client.get("/check_overtime/1", headers=boss)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Permission denied."
    }