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

def test_put_leave_success():
    leave = {
        'start': '2021-08-02T13:00:23.535Z',
        'end': '2021-08-02T17:00:23.535Z',
        'category': '事假',
        'reason': 'Bubba'
        }
    leave_json = json.dumps(leave)
    response = client.put("/leave/1", data=leave_json, headers=officer)
    print(response.json())
    assert response.status_code == 200

def test_put_leave_wronguser():
    leave = {
        'start': '2021-08-02T13:00:23.535Z',
        'end': '2021-08-02T17:00:23.535Z',
        'category': '事假',
        'reason': '錯誤的使用者'
        }
    leave_json = json.dumps(leave)
    response = client.put("/leave/1", data=leave_json, headers=manager)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Wrong User."
    }

def test_put_leave_failed():
    leave = {
        'start': '2021-07-29T08:00:23.535Z',
        'end': '2021-07-00T17:00:23.535Z',
        'category': '特休',
        'reason': '特休'
        }
    leave_json = json.dumps(leave)
    response = client.put("/leave/2", data=leave_json, headers=officer)
    assert response.status_code == 422

def test_put_leave_wrongtype():
    leave = {
        'start': '2021-08-01T08:00:23.535Z',
        'end': '2021-08-01T17:00:23.535Z',
        'category': '不對的type',
        'reason': ''
        }
    leave_json = json.dumps(leave)
    response = client.put("/leave/5", data=leave_json, headers=boss)
    assert response.status_code == 422

def test_put_leave_wrongday():
    leave = {
        'start': '2021-08-01T08:00:23.535Z',
        'end': '2021-08-02T17:00:23.535Z',
        'category': '事假',
        'reason': '不要在假日請假'
        }
    leave_json = json.dumps(leave)
    response = client.put("/leave/3", data=leave_json, headers=boss)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "start and end shouldn't at the day of Day Off."
    }

def test_put_leave_wrongday2():
    leave = {
        'start': '2021-07-30T08:00:23.535Z',
        'end': '2021-08-01T17:00:23.535Z',
        'category': '事假',
        'reason': '町田唱歌好聽'
        }
    leave_json = json.dumps(leave)
    response = client.put("/leave/2", data=leave_json, headers=boss)
    print(response.json())
    assert response.status_code == 400
    assert response.json() == {
        "detail": "start and end shouldn't at the day of Day Off."
    }

def test_put_leave_wrongday3():
    leave = {
        'start': '2021-08-03T08:00:23.535Z',
        'end': '2021-08-02T17:00:23.535Z',
        'category': '病假',
        'reason': '吃壞肚子了'
        }
    leave_json = json.dumps(leave)
    response = client.put("/leave/5", data=leave_json, headers=boss)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Wrong day."
    }

def test_put_leave_wrongtime():
    leave = {
        'start': '2021-08-03T08:00:23.535Z',
        'end': '2021-08-03T18:00:23.535Z',
        'category': '事假',
        'reason': '真是嚴格的格式啊'
        }
    leave_json = json.dumps(leave)
    response = client.put("/leave/5", data=leave_json, headers=boss)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "start and end can't after 17:00"
    }

def test_put_leave_wrongtime2():
    leave = {
        'start': '2021-08-02T07:00:23.535Z',
        'end': '2021-08-02T17:00:23.535Z',
        'category': '事假',
        'reason': '希望我這禮拜能完成'
        }
    leave_json = json.dumps(leave)
    response = client.put("/leave/4", data=leave_json, headers=boss)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "start and end can't before 8:00"
    }

def test_put_leave_notfound():
    leave = {
        'start': '2021-08-11T08:00:23.535Z',
        'end': '2021-08-11T17:00:23.535Z',
        'category': '事假',
        'reason': 'puipui'
        }
    leave_json = json.dumps(leave)
    response = client.put("/leave/20", data=leave_json, headers=boss)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Leave not found"
    }