from abc import ABC, abstractmethod
from sqlmodel import Session
from app.models.trade_model import Trade
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExecutionHandler(ABC):
    @abstractmethod
    def execute_order(self, db: Session, ticker: str, side: str, quantity: int, price: float, owner_id: int):
        pass

class PaperExecutionHandler(ExecutionHandler):
    def execute_order(self, db: Session, ticker: str, side: str, quantity: int, price: float, owner_id: int):
        
        logger.info(f"PAPER TRADE: User {owner_id} {side} {quantity} {ticker} @ ${price}")

        trade = Trade(
            owner_id=owner_id,
            ticker=ticker,
            side=side,
            quantity=quantity,
            price=price,
            timestamp=datetime.now(timezone.utc),
            status="FILLED"
        )
        db.add(trade)
        db.commit()
        db.refresh(trade)
        
        return trade