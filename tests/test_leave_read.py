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
def test_get_leaves_officer():
    response = client.get("/leave", headers=officer)
    print(response.json())
    assert response.status_code == 200

def test_get_leaves_manager():
    response = client.get("/leave", headers=manager)
    print(response.json())
    assert response.status_code == 200

def test_get_leave_officer():
    response = client.get("/leave/1", headers=officer)
    assert response.status_code == 200

def test_get_leave_manager():
    response = client.get("/leave/1", headers=manager)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Wrong user."
    }

def test_get_leave_notfound():
    response = client.get("/leave/20", headers=manager)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "not found."
    }

#check manager
def test_check_leaves_manager():
    response = client.get("/check_leave", headers=manager)
    print(response.json())
    assert response.status_code == 200

def test_check_leave_manager():
    response = client.get("/check_leave/1", headers=manager)
    print(response.json())
    assert response.status_code == 200

def test_check_leave_notfound():
    response = client.get("/check_leave/20", headers=manager)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Permission denied."
    }

def test_check_leave_hr():
    response = client.get("/check_leave/3", headers=manager)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Permission denied."
    }

def test_check_leave_self():
    response = client.get("/check_leave/2", headers=manager)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Permission denied."
    }

#check officer
def test_check_leaves_officer():
    response = client.get("/check_leave", headers=officer)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You are not a manager."
    }

def test_check_leave_officer():
    response = client.get("/check_leave/1", headers=officer)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You are not a manager."
    }

#check boss
def test_check_leaves_boss():
    response = client.get("/check_leave", headers=boss)
    assert response.status_code == 200
    print(response.json())

def test_check_leave_boss():
    response = client.get("/check_leave/2", headers=boss)
    assert response.status_code == 200
    print(response.json())

def test_check_leave_bossself():
    response = client.get("/check_leave/5", headers=boss)
    assert response.status_code == 200
    print(response.json())

def test_check_leave_boss_staff():
    response = client.get("/check_leave/1", headers=boss)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Permission denied."
    }