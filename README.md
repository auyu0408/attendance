# Attendance back end  

I separated attendance-system and use fastAPI to write back end.

## Prerequisites  

- Python 3.8  
- pipenv(Python Module)  

## Set up

### Environment Setup  

1. initialize python environment  

```lan=bash  
make init
```
  
2. Start the service  

```lan=bash
make start
pipenv run uvicorn attendance.main:app --reload
```  
  
- Back end docs will run at [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/)  

3. Stop service  

```
Ctrl+c
```  
  
4. Delete Database  

```lan=bash
make clean
```  

## Development  

### testing  

Using `pytest` in fastapi.  

```lan=bash
pipenv shell
pip install requests
make test
```

## First time to use  

- We already set an admin account when we do `make init` it, there is the info.

```
name: admin
account: admin
password: admin
```
