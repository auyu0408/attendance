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

def test_put_staff_success():
    user = {
        'account': 'officer1',
        'name': 'rushia boing boing',
        'email': 'uruharushia@gmail.com',
        'department': '業務部',
        'manager': False,
        'hr': False,
        'on_job': '2000-07-18',
        'status': 0
        }
    user_json = json.dumps(user)
    response = client.put("/hr/users/2", data=user_json, headers=admin)
    assert response.status_code == 200
    print(response.json())

def test_put_staff_staff():
    user = {
        'account': 'manager1',
        'name': 'amesame',
        'email': 'a@gmail.com',
        'department': '業務部',
        'manager': True,
        'hr': False,
        'on_job': '2003-06-22',
        'status': 0
        }
    user_json = json.dumps(user)
    response = client.put("/hr/users/3", data=user_json, headers=officer)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Your are not hr."
    }

def test_put_staff_conflict():
    user = {
        'account': 'manager1',
        'name': 'amelia',
        'email': 'smoleame@gmail.com',
        'department': '人事部',
        'manager': False,
        'hr': True,
        'on_job': '2015-09-13',
        'status': 0
        }
    user_json = json.dumps(user)
    response = client.put("/hr/users/4", data=user_json, headers=admin)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Account is conflict."
    }

def test_put_staff_notfound():
    user = {
        'account': 'hr2',
        'name': 'amelia',
        'email': 'hana@gmail.com',
        'department': '人事部',
        'manager': False,
        'hr': True,
        'on_job': '2015-09-13',
        'status': 0
        }
    user_json = json.dumps(user)
    response = client.put("/hr/users/10", data=user_json, headers=admin)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found."
    }

def test_put_staff_resigned():
    user = {
        'account': 'baaqua',
        'name': 'amelia',
        'email': 'minato@gmail.com',
        'department': '人事部',
        'manager': False,
        'hr': True,
        'on_job': '2015-09-13',
        'status': 0
        }
    user_json = json.dumps(user)
    response = client.put("/hr/users/7", data=user_json, headers=admin)
    assert response.status_code == 403
    assert response.json() == {
        "detail": "User is resigned, the file can't edit."
    }

def test_put_staff_wrongway():
    user = {
        'account': '35P',
        'name': 'amelia',
        'email': 'sakuramiko@gmail.com',
        'department': '人事部',
        'manager': False,
        'hr': True,
        'on_job': '2015-09-13',
        'status': 2
        }
    user_json = json.dumps(user)
    response = client.put("/hr/users/4", data=user_json, headers=admin)
    assert response.status_code == 403
    assert response.json() == {
        "detail": "Wrong request way."
    }