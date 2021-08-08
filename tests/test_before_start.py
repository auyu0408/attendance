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
header = {"accept": "application/json", "Authorization": "Bearer admin"}

def test_get_init_user():
    response = client.post("/get_init_user")
    assert response.status_code == 201 or response.status_code == 204

def test_profile():
    response = client.get("/hr/users", headers=header)
    assert response.status_code == 200
    print(response.json())
