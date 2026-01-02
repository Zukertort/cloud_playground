from fastapi import APIRouter, Depends, Security, HTTPException
from sqlmodel import Session, select
from app.database import get_db
from app.models.user_model import User
from app.dependencies import get_current_user
from app.services.execution import PaperExecutionHandler
from app.services.alpaca_handler import AlpacaExecutionHandler
from app.schemas.trade import TradeRequest
from typing import List
from app.models.trade_model import Trade

router = APIRouter(
    prefix="/trade",
    tags=["Trade"],
    dependencies=[Depends(get_current_user)]
)

execution_handler = AlpacaExecutionHandler()

@router.post("/execute")
async def execute_order(
    trade_request: TradeRequest,
    current_user: User = Security(get_current_user),
    db: Session = Depends(get_db)
): 
    try:
        executed_trade = execution_handler.execute_order(
            db=db,
            ticker=trade_request.ticker,
            side=trade_request.side,
            quantity=trade_request.quantity,
            price=trade_request.price,
            owner_id=current_user.id
        )
        return executed_trade
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution Failed: {str(e)}")
    
@router.get("/history", response_model=List[Trade])
async def get_trade_history(
    current_user: User = Security(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fetch execution history for the current user.
    """
    statement = select(Trade).where(Trade.owner_id == current_user.id).order_by(Trade.timestamp.desc())
    results = db.exec(statement).all()
    return results