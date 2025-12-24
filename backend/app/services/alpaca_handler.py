from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from app.services.execution import ExecutionHandler
from app.settings import settings
from sqlmodel import Session
import datetime
from datetime import timezone
import logging

logger = logging.getLogger(__name__)

class AlpacaExecutionHandler(ExecutionHandler):
    def __init__(self):
        self.client = TradingClient(
            settings.ALPACA_API_KEY, 
            settings.ALPACA_SECRET_KEY, 
            paper=True
        )
        
    def execute_order(self, db: Session, ticker: str, side: str, quantity: int, price: float, owner_id: int):
        """
        Sends order to Alpaca (Paper Trading) via SDK
        """
        logger.info(f"Sending {side} order for {ticker} to Alpaca...")
        
        try:
            market_order_data = MarketOrderRequest(
                symbol=ticker,
                qty=quantity,
                side=OrderSide.BUY if side.upper() == "BUY" else OrderSide.SELL,
                time_in_force=TimeInForce.GTC
            )

            order = self.client.submit_order(order_data=market_order_data)
            
            logger.info(f"Alpaca accepted order: {order.id}")
            
            from app.models.trade_model import Trade
            
            trade = Trade(
                owner_id=owner_id,
                ticker=ticker,
                side=side,
                quantity=quantity,
                price=price,
                timestamp=datetime.datetime.now(datetime.timezone.utc),
                status="SUBMITTED"
            )

            db.add(trade)
            db.commit()
            db.refresh(trade)
            
            return trade
            
        except Exception as e:
            logger.error(f"Alpaca Order Failed: {e}")
            raise e