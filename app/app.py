from typing import Optional
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
import logging
from CityAutoCompleter.CityAutoCompleter import CityAutoCompleter
from schema.location import Location

logger = logging.getLogger(__name__)
auto_completer = CityAutoCompleter()

app = FastAPI(
    title="City Autocomplete API",
    description="API for autocompleting city names based on prefix and optional coordinates.",
    version="1.0.0"
)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

@app.get("/suggestions", description="Autocomplete city names based on prefix and optional location")
async def get_suggestions(location: Location = Depends()):
    try: 
        logger.info(f"Searching for city with q={location.q}, latitude={location.lat}, longitude={location.long}")
        cities = auto_completer.suggest(prefix=location.q, user_lat=location.lat, user_lon=location.long)
        return {"suggestions": cities}
    except Exception as e:
        logger.exception(f"An exception occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
