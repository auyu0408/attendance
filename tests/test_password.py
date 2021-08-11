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
header = { "accept": "*/*", "Authorization": "Bearer officer1", "Content-Type": "application/json"}

def test_passwd_success():
    passwd = {
        "origin": "officer1",
        "new": "meowmeowmeow"
    }
    response = client.put("/password", json=passwd, headers=header)
    assert response.status_code == 204

def test_passwd_failed():
    passwd = {
        "origin": "patten",
        "new": "rushia_boing_boing"
    }
    response = client.put("/password", headers=header, json=passwd)
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Wrong password."
    }