from fastapi import APIRouter, HTTPException, Depends
import numpy as np
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.model_loader import global_model_loader

router = APIRouter(
    prefix="/model",
    tags=["Model"]
)

@router.post("/", response_model=PredictionResponse)
async def predict_alpha(request: PredictionRequest):
    """
    Predicts alpha for a given ticker.
    """
    try:
        model = global_model_loader.get_model(request.ticker)
        features_array = np.array(request.features).reshape(1, -1)
        pred_class = model.predict(features_array)[0]
        probs = model.predict_proba(features_array)[0]

        confidence = probs[pred_class]

        signal_map = {
            0: "SELL/IGNORE",
            1: "BUY",}
        
        return PredictionResponse(
            ticker=request.ticker,
            signal=signal_map[int(pred_class)],
            confidence=float(confidence)
        )
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Model for ticker {request.ticker} not trained yet.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")