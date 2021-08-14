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
admin = {"accept": "application/json", "Authorization": "Bearer admin", "Content-Type": "application/json"}

def test_create_daily_admin():
    daily = {
        'day': '2021-08-10',
        'on': '08:00',
        'off': '08:00',
        'on_fix': '08:00',
        'off_fix': '08:00',
        'fix_note': '他會成功',
        'user_id': 2
    }
    daily_json = json.dumps(daily)
    response = client.post("/hr/daily", data=daily_json, headers=admin)
    assert response.status_code == 201
    print(response.json())

def test_create_daily_success():
    daily = {
        'day': '2021-08-11',
        'on': '08:00',
        'off': '08:00',
        'on_fix': '08:00',
        'off_fix': '08:00',
        'fix_note': '他會成功',
        'user_id': 2
    }
    daily_json = json.dumps(daily)
    response = client.post("/hr/daily", data=daily_json, headers=admin)
    assert response.status_code == 201
    print(response.json())

def test_create_daily_staff():
    daily = {
        'day': '2021-08-10',
        'on': '08:00',
        'off': '08:00',
        'on_fix': '08:00',
        'off_fix': '08:00',
        'fix_note': '他會失敗',
        'user_id': 2
    }
    daily_json = json.dumps(daily)
    response = client.post("/hr/daily", data=daily_json, headers=officer)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You are not hr."
    }

def test_create_daily_wrongtime():
    daily = {
        'day': '2021-08-10',
        'on': '09:00',
        'off': '08:00',
        'on_fix': '08:00',
        'off_fix': '08:00',
        'fix_note': '預計會失敗',
        'user_id': 4
    }
    daily_json = json.dumps(daily)
    response = client.post("/hr/daily", data=daily_json, headers=admin)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Wrong time"
    }

def test_create_daily_wrongid():
    daily = {
        'day': '2021-08-10',
        'on': '08:00',
        'off': '17:00',
        'on_fix': '08:00',
        'off_fix': '17:00',
        'fix_note': '就是會失敗',
        'user_id': 10
    }
    daily_json = json.dumps(daily)
    response = client.post("/hr/daily", data=daily_json, headers=admin)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "User_id not found."
    }

def test_create_daily_wrongtype():
    daily = {
        'day': '2021-08-10',
        'on': 'string',
        'off': 'string',
        'on_fix': 'string',
        'off_fix': 'string',
        'fix_note': 'string',
        'user_id': 2
    }
    daily_json = json.dumps(daily)
    response = client.post("/hr/daily", data=daily_json, headers=admin)
    assert response.status_code == 422