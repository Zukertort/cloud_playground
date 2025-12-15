from pydantic import BaseModel
from typing import List, Optional

class HistoryPoint(BaseModel):
    timestamp: str
    close: float

class DashboardResponse(BaseModel):
    ticker: str
    current_price: float
    signal: str
    meta_signal: str
    confidence: float
    history: List[HistoryPoint]
    sentiment_score: float
    sentiment_analysis: str
    news_headlines: List[str]