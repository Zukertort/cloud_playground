from pydantic import BaseModel
from typing import List

class PredictionRequest(BaseModel):
    ticker: str
    features: List[float]

class PredictionResponse(BaseModel):
    ticker: str
    signal: str
    meta_signal: str
    confidence: float