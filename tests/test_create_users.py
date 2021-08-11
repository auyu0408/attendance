from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.orm import Session

from attendance.main import app, login
from attendance import crud
from attendance.database import get_db
import json

client = TestClient(app)

async def override_dependency(form_data: OAuth2PasswordRequestForm= Depends(), db:Session=Depends(get_db)):
    user_dict = crud.authenticate_user(db, account=form_data.username, passwd=form_data.password)
    return {"access_token": user_dict.account, "token_type": "bearer"}

app.dependency_overrides[login] = override_dependency
header = {"accept": "application/json", "Authorization": "Bearer admin", "Content-Type": "application/json"}
header_staff = {"accept": "application/json", "Authorization": "Bearer officer1", "Content-Type": "application/json"}

def test_create_user_success():
    user = {
        'account': 'officer1',
        'passwd': 'officer1',
        'name': 'rushia',
        'email': 'uruharushia@gmail.com',
        'department': '業務部',
        'manager': False,
        'hr': False,
        'on_job': '2000-07-18',
        'off_job': '2021-08-08'
        }
    user_json = json.dumps(user)
    response = client.post("/hr/users", data=user_json, headers=header)
    assert response.status_code == 201

def test_create_staff():
    user = {
        'account': 'akkihaato',
        'passwd': 'haachama',
        'name': 'haachamachama',
        'email': 'haachama@gmail.com',
        'department': '這個會失敗',
        'manager': False,
        'hr': False,
        'on_job': '2001-08-10',
        'off_job': '2021-08-08'
        }
    user_json = json.dumps(user)
    response = client.post("/hr/users", data=user_json, headers=header_staff)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Your are not hr."
    }

def test_create_staff_conflict():
    user = {
        'account': 'officer1',
        'passwd': 'officer',
        'name': 'yabe',
        'email': 'fubuki@gmail.com',
        'department': '這個會失敗',
        'manager': False,
        'hr': False,
        'on_job': '2000-07-18',
        'off_job': '2021-08-08'
        }
    user_json = json.dumps(user)
    response = client.post("/hr/users", data=user_json, headers=header)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Account is conflict."
    }

def test_create_manager():
    user = {
        'account': 'manager1',
        'passwd': 'manager1',
        'name': 'gura',
        'email': 'a@gmail.com',
        'department': '業務部',
        'manager': True,
        'hr': False,
        'on_job': '2003-06-22',
        'off_job': '2021-08-08'
        }
    user_json = json.dumps(user)
    response = client.post("/hr/users", data=user_json, headers=header)
    assert response.status_code == 201
    print(response.json())

def test_create_hr():
    user = {
        'account': 'hr1',
        'passwd': 'hr1',
        'name': 'amelia',
        'email': 'smoleame@gmail.com',
        'department': '人事部',
        'manager': False,
        'hr': True,
        'on_job': '2015-09-13',
        'off_job': '2021-08-08'
        }
    user_json = json.dumps(user)
    response = client.post("/hr/users", data=user_json, headers=header)
    assert response.status_code == 201
    print(response.json())

def test_create_hr_manager():
    user = {
        'account': 'hrmanager1',
        'passwd': 'hrmanager1',
        'name': 'moona',
        'email': 'adamoona@gmail.com',
        'department': '人事部',
        'manager': True,
        'hr': True,
        'on_job': '2010-04-11',
        'off_job': '2021-08-08'
        }
    user_json = json.dumps(user)
    response = client.post("/hr/users", data=user_json, headers=header)
    assert response.status_code == 201
    print(response.json())

def test_create_boss():
    user = {
        'account': 'boss1',
        'passwd': 'boss1',
        'name': 'pekora',
        'email': 'konpeko@gmail.com',
        'department': 'Boss',
        'manager': True,
        'hr': True,
        'on_job': '1999-07-17',
        'off_job': '2021-08-08'
        }
    user_json = json.dumps(user)
    response = client.post("/hr/users", data=user_json, headers=header)
    assert response.status_code == 201
    print(response.json())

def test_create_officer2():
    user = {
        'account': 'officer2',
        'passwd': 'officer2',
        'name': 'nakiri ayame',
        'email': 'docchidocchi@gmail.com',
        'department': 'Boss',
        'manager': False,
        'hr': False,
        'on_job': '2018-09-03',
        'off_job': '2021-08-08'
        }
    user_json = json.dumps(user)
    response = client.post("/hr/users", data=user_json, headers=header)
    assert response.status_code == 201
    print(response.json())