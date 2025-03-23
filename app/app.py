from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get('/')
def read_root():
    return {"Hello": "World"}

@app.get("/suggestions/{query_param}")
def read_item(query_param: str, q: Union[str, None], lat: Union[float, None] = None, long: Union[float, None] = None):
    return {"item_id": query_param, "q": q}