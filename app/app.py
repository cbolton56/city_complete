from typing import Optional
from fastapi import FastAPI

from CityAutoCompleter.CityAutoCompleter import CityAutoCompleter

auto_completer = CityAutoCompleter()

app = FastAPI()

@app.get('/')
async def read_root():
    return {"Hello": "World"}

@app.get("/suggestions")
async def get_suggestions(q: str, lat: Optional[str] = None, long: Optional[str] = None):
    cities = auto_completer.suggest(prefix=q, user_lat=lat, user_lon=long)
    return {"suggestions": cities}
