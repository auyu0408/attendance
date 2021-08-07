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
  2. Start the service  
  ```
  pipenv run uvicorn attendance.main:app --reload
  ```  
  - The server will run at [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/)  

  3. Stop service  
  ```
  Ctrl+c
  ```  
  4. Delete Database  
  ```
  make clean
  ```  