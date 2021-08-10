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

def test_create_leave_success():
    leave = {
        'start': '2021-08-02T13:00:23.535Z',
        'end': '2021-08-02T17:00:23.535Z',
        'category': '事假',
        'reason': '處理私事'
        }
    leave_json = json.dumps(leave)
    response = client.post("/leave", data=leave_json, headers=officer)
    print(response.json())
    assert response.status_code == 201

def test_create_leave_manager():
    leave = {
        'start': '2021-08-02T08:00:23.535Z',
        'end': '2021-08-06T17:00:23.535Z',
        'category': '出差',
        'reason': '展覽'
        }
    leave_json = json.dumps(leave)
    response = client.post("/leave", data=leave_json, headers=manager)
    assert response.status_code == 201

def test_create_leave_hr():
    leave = {
        'start': '2021-07-29T08:00:23.535Z',
        'end': '2021-08-02T17:00:23.535Z',
        'category': '家庭照顧假',
        'reason': '幼稚園消毒'
        }
    leave_json = json.dumps(leave)
    response = client.post("/leave", data=leave_json, headers=hr)
    assert response.status_code == 201

def test_create_leave_hr_manager():
    leave = {
        'start': '2021-08-09T08:00:23.535Z',
        'end': '2021-08-10T17:00:23.535Z',
        'category': '事假',
        'reason': '處理私事'
        }
    leave_json = json.dumps(leave)
    response = client.post("/leave", data=leave_json, headers=hr_manager)
    assert response.status_code == 201

def test_create_leave_boss():
    leave = {
        'start': '2021-08-05T08:00:23.535Z',
        'end': '2021-08-05T17:00:23.535Z',
        'category': '事假',
        'reason': '處理私事'
        }
    leave_json = json.dumps(leave)
    response = client.post("/leave", data=leave_json, headers=boss)
    assert response.status_code == 201

def test_create_leave_failed():
    leave = {
        'start': '2021-07-29T08:00:23.535Z',
        'end': '2021-07-00T17:00:23.535Z',
        'category': '特休',
        'reason': '特休'
        }
    leave_json = json.dumps(leave)
    response = client.post("/leave", data=leave_json, headers=officer)
    assert response.status_code == 422

def test_create_leave_wrongtype():
    leave = {
        'start': '2021-08-01T08:00:23.535Z',
        'end': '2021-08-01T17:00:23.535Z',
        'category': '不對的type',
        'reason': ''
        }
    leave_json = json.dumps(leave)
    response = client.post("/leave", data=leave_json, headers=boss)
    assert response.status_code == 422

def test_create_leave_wrongday():
    leave = {
        'start': '2021-08-01T08:00:23.535Z',
        'end': '2021-08-02T17:00:23.535Z',
        'category': '事假',
        'reason': '處理私事'
        }
    leave_json = json.dumps(leave)
    response = client.post("/leave", data=leave_json, headers=boss)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "start or end shouldn't at the day of Day Off."
    }

def test_create_leave_wrongday2():
    leave = {
        'start': '2021-07-30T08:00:23.535Z',
        'end': '2021-08-01T17:00:23.535Z',
        'category': '事假',
        'reason': '處理私事'
        }
    leave_json = json.dumps(leave)
    response = client.post("/leave", data=leave_json, headers=boss)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "start or end shouldn't at the day of Day Off."
    }

def test_create_leave_wrongday3():
    leave = {
        'start': '2021-08-03T08:00:23.535Z',
        'end': '2021-08-02T17:00:23.535Z',
        'category': '事假',
        'reason': '處理私事'
        }
    leave_json = json.dumps(leave)
    response = client.post("/leave", data=leave_json, headers=boss)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Wrong day."
    }

def test_create_leave_wrongtime():
    leave = {
        'start': '2021-08-03T08:00:23.535Z',
        'end': '2021-08-03T18:00:23.535Z',
        'category': '事假',
        'reason': '處理私事'
        }
    leave_json = json.dumps(leave)
    response = client.post("/leave", data=leave_json, headers=boss)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "start and end can't after 17:00"
    }

def test_create_leave_wrongtime2():
    leave = {
        'start': '2021-08-02T07:00:23.535Z',
        'end': '2021-08-02T17:00:23.535Z',
        'category': '事假',
        'reason': '處理私事'
        }
    leave_json = json.dumps(leave)
    response = client.post("/leave", data=leave_json, headers=boss)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "start and end can't before 8:00"
    }