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

admin = {"accept": "application/json", "Authorization": "Bearer admin", "Content-Type": "application/json"}
officer = {"accept": "application/json", "Authorization": "Bearer officer1", "Content-Type": "application/json"}

def test_dayoff_success():
    dayoff = {
        'day': '2021-08-01',
        'type': 7
    }
    dayoff_json = json.dumps(dayoff)
    response = client.post("/hr/day_off", data=dayoff_json, headers=admin)
    assert response.status_code == 201

def test_dayoff_create():
    dayoff = {
        'day': '2021-07-31',
        'type': 6
    }
    dayoff_json = json.dumps(dayoff)
    response = client.post("/hr/day_off", data=dayoff_json, headers=admin)
    assert response.status_code == 201

def test_dayoff_failed():
    dayoff = {
        'day': '2021-07-00',
        'type': 6
    }
    dayoff_json = json.dumps(dayoff)
    response = client.post("/hr/day_off", data=dayoff_json, headers=admin)
    assert response.status_code == 422

def test_dayoff_staff():
    dayoff = {
        'day': '2021-07-31',
        'type': 6
    }
    dayoff_json = json.dumps(dayoff)
    response = client.post("/hr/day_off", data=dayoff_json, headers=officer)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "You are not hr."
    }

def test_dayoff_repeated():
    dayoff = {
        'day': '2021-07-31',
        'type': 6
    }
    dayoff_json = json.dumps(dayoff)
    response = client.post("/hr/day_off", data=dayoff_json, headers=admin)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Reapeat day."
    }