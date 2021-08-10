# attendance back end  
I separated attendance-system and use fastAPI to write backend

## Set up  

### Prerequisites  

- Python 3.8  
- pipenv(Python Module)  

### Environment Setup  

  1. initialize python environment  
  ```
  make init
  ```  
  - then, press `Ctrl+C`.
  2. Setup admin
  ```
  make setup
  ```
  3. Start the service  
  ```
  pipenv run uvicorn attendance.main:app --reload
  ```  
  - Back end docs will run at [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/)  

  4. Stop service  
  ```
  Ctrl+c
  ```  
  5. Delete Database  
  ```
  make clean
  ```  

### First time use:

You need to click `post /get_admin` to get an admin.  
admin account and password:
```
name: admin
account: admin
password: admin
```