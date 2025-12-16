from pydantic import BaseModel

class TradeRequest(BaseModel):
    ticker: str
    side: str
    quantity: int
    price: float