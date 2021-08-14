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
admin = {"accept": "application/json", "Authorization": "Bearer admin", "Content-Type": "application/json"}
officer = {"accept": "application/json", "Authorization": "Bearer officer1", "Content-Type": "application/json"}

def test_delete_staff_success():
    response = client.delete("/leave/6", headers=officer)
    assert response.status_code == 204

def test_delete_staff_notfound():
    response = client.delete("/leave/10", headers=officer)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Leave not found."
    }

def test_delete_wrong():
    response = client.delete("/leave/4", headers=admin)
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Wrong user."
    }