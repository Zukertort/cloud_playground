import quant_engine
from ..schemas.analytics import VolatilityRequest, VolatilityResponse
from fastapi import APIRouter, HTTPException, Depends
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=VolatilityResponse)
async def calculate_volatility(request: VolatilityRequest):
    if request.window < 2:
        raise HTTPException(status_code=400, detail="Volatility requires at least 2 data points.")
    try:
        result = quant_engine.calculate_volatility(request.prices, request.window)
        return {"values": result}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")