from fastapi import FastAPI, Query, Path

app = FastAPI()

@app.get("/user ")
async def user(
    *,
    user_id: int = Query(..., title="The id of the user to get", gt=0)
):
    return {'user_id':user_id}

@app.get("/leave/{leave_id}")
async def user(
    *,
    leave_id: int = Path(..., title="the id of the user to get", gt=0)
):
    return {'leave_id':leave_id}

@app.post('/user/{user_id}')
async def update_user(
    *,
    user_id: int, 
    really_update: int = Query(...)
):
    pass