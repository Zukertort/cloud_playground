from pydantic import BaseModel
from typing import List

class VolatilityRequest(BaseModel):
    prices: List[float]
    window: int = 10

class VolatilityResponse(BaseModel):
    values: List[float]