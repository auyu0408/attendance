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

officer = {"accept": "application/json", "Authorization": "Bearer officer1", "Content-Type": "application/json"}
manager = {"accept": "application/json", "Authorization": "Bearer manager1", "Content-Type": "application/json"}
hr = {"accept": "application/json", "Authorization": "Bearer hr1", "Content-Type": "application/json"}
hr_manager = {"accept": "application/json", "Authorization": "Bearer hrmanager1", "Content-Type": "application/json"}
boss = {"accept": "application/json", "Authorization": "Bearer boss1", "Content-Type": "application/json"}

def test_create_overtime_officer():
    overtime = {
        'day': '2021-08-07',
        'start': '13:00',
        'end': '17:00',
        'reason': '處理私事',
        }
    overtime_json = json.dumps(overtime)
    response = client.post("/overtime", data=overtime_json, headers=officer)
    print(response.json())
    assert response.status_code == 201

def test_create_overtime_manager():
    overtime = {
        'day': '2021-07-28',
        'start': '17:30',
        'end': '19:00',
        'reason': '廠協會開會',
        }
    overtime_json = json.dumps(overtime)
    response = client.post("/overtime", data=overtime_json, headers=manager)
    print(response.json())
    assert response.status_code == 201

def test_create_overtime_hr():
    overtime = {
        'day': '2021-08-10',
        'start': '17:30',
        'end': '19:00',
        'reason': '廠協會開會',
        }
    overtime_json = json.dumps(overtime)
    response = client.post("/overtime", data=overtime_json, headers=hr)
    print(response.json())
    assert response.status_code == 201

def test_create_overtime_hr_manager():
    overtime = {
        'day': '2021-08-06',
        'start': '17:30',
        'end': '19:30',
        'reason': '薪資核對',
        }
    overtime_json = json.dumps(overtime)
    response = client.post("/overtime", data=overtime_json, headers=hr)
    print(response.json())
    assert response.status_code == 201

def test_create_overtime_boss():
    overtime = {
        'day': '2021-08-07',
        'start': '8:00',
        'end': '12:00',
        'reason': '廠商驗貨',
        }
    overtime_json = json.dumps(overtime)
    response = client.post("/overtime", data=overtime_json, headers=boss)
    print(response.json())
    assert response.status_code == 201

def test_create_overtime_wrongtime():
    overtime = {
        'day': '2021-08-08',
        'start': '17:00',
        'end': '19:00',
        'reason': '他就會錯',
        }
    overtime_json = json.dumps(overtime)
    response = client.post("/overtime", data=overtime_json, headers=officer)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Wrong start time."
    }

def test_create_overtime_wrongtime2():
    overtime = {
        'start': '2021-08-02T17:00:23.535Z',
        'end': '2021-08-02T19:00:23.535Z',
        'reason': '我就爛',
        }
    overtime_json = json.dumps(overtime)
    response = client.post("/overtime", data=overtime_json, headers=officer)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Wrong start time."
    }

def test_create_overtime_wrongtime3():
    overtime = {
        'start': '2021-08-02T13:00:23.535Z',
        'end': '2021-08-02T08:00:23.535Z',
        'reason': '他也要錯',
        }
    overtime_json = json.dumps(overtime)
    response = client.post("/overtime", data=overtime_json, headers=officer)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Wrong time."
    }