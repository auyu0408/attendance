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
header = {"accept": "application/json", "Authorization": "Bearer admin", "Content-Type": "application/json"}
header_staff = {"accept": "application/json", "Authorization": "Bearer officer", "Content-Type": "application/json"}

def test_create_user_success():
    user = {
        "account": "officer",
        "passwd": "offficer",
        "name": "rushia",
        "email": "uruharushia@gmail.com",
        "department": "業務部",
        "manager": False,
        "hr": False,
        "on_job": "2000-07-18",
        "off_job": "2021-08-08"
    }
    response = client.post("/hr/users", data=user, headers=header)
    print(response.json())
    assert response.status_code == 200