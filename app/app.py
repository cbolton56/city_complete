from typing import Optional
from fastapi import FastAPI

from FuzzyCitySearch.FuzzyCitySearch import FuzzyCitySearch

fuzzy_search = FuzzyCitySearch()
app = FastAPI()

@app.get('/')
async def read_root():
    return {"Hello": "World"}

@app.get("/suggestions")
async def get_suggestions(q: str, lat: Optional[str] = None, long: Optional[str] = None):
    cities = fuzzy_search.search(query=q, query_lat=lat, query_lon=long)
    return {"suggestions": cities}
