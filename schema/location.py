# pydantic model for get endpoint
from pydantic import (
    BaseModel,
    Field,
)
from typing import Optional

class Location(BaseModel):
    """Pydantic model for API """
    q: str = Field(..., description="Complete or prefix of city to auto complete")
    lat: Optional[float] = Field(None, description="Latitude of the location")
    long: Optional[float] = Field(None, description="Longitude of the location")
