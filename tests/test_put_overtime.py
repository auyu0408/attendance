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

def test_put_overtime_officer():
    overtime = {
        'day': '2021-08-07',
        'start': '13:00',
        'end': '17:00',
        'reason': '加班時間並不會處理私事'
        }
    overtime_json = json.dumps(overtime)
    response = client.put("/overtime/1", data=overtime_json, headers=officer)
    print(response.json())
    assert response.status_code == 200

def test_put_overtime_wronguser():
    overtime = {
        'day': '2021-08-07',
        'start': '13:00',
        'end': '17:00',
        'reason': '假日被迫工程掠地'
        }
    overtime_json = json.dumps(overtime)
    response = client.put("/overtime/1", data=overtime_json, headers=manager)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Wrong User."
    }

def test_put_overtime_wrongtime():
    overtime = {
        'day': '2021-08-08',
        'start': '17:00',
        'end': '19:00',
        'reason': '錯誤的開始'
        }
    overtime_json = json.dumps(overtime)
    response = client.put("/overtime/1", data=overtime_json, headers=officer)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Wrong start time."
    }

def test_put_overtime_wrongtime2():
    overtime = {
        'day': '2021-08-02',
        'start': '17:00',
        'end': '19:00',
        'reason': 'P.H.'
        }
    overtime_json = json.dumps(overtime)
    response = client.put("/overtime/1", data=overtime_json, headers=officer)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Wrong start time."
    }

def test_put_overtime_wrongtime3():
    overtime = {
        'day': '2021-08-01',
        'start': '13:00',
        'end': '08:00',
        'reason': '圓周率之花'
        }
    overtime_json = json.dumps(overtime)
    response = client.put("/overtime/3", data=overtime_json, headers=hr)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Wrong time."
    }

def test_put_overtime_notfound():
    overtime = {
        'day': '2021-08-01',
        'start': '13:00',
        'end': '17:00',
        'reason': '圓周率之花'
        }
    overtime_json = json.dumps(overtime)
    response = client.put("/overtime/20", data=overtime_json, headers=hr)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Overtime not found."
    }