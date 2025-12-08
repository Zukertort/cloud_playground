from fastapi import APIRouter, HTTPException, Depends
import numpy as np
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.model_loader import global_model_loader
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/predict",
    tags=["Model"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=PredictionResponse)
async def predict_alpha(request: PredictionRequest):
    """
    Predicts alpha for a given ticker.
    """
    try:
        models = global_model_loader.get_model(request.ticker)
        primary_model = models["model"]
        meta_model = models["meta_model"]
        features_array = np.array(request.features).reshape(1, -1)

        primary_pred = primary_model.predict(features_array)[0]
        primary_probs = primary_model.predict_proba(features_array)

        primary_conf = np.max(primary_probs, axis=1).reshape(-1, 1)
        meta_features = np.hstack([features_array, primary_conf])

        meta_pred = meta_model.predict(meta_features)[0]
        meta_probs = meta_model.predict_proba(meta_features)[0]

        signal_map = {
            0: "SELL/IGNORE",
            1: "BUY",}
        
        final_signal_code = 0
        if primary_pred == 1 and meta_pred == 1:
            final_signal_code = 1
        
        return PredictionResponse(
            ticker=request.ticker,
            signal=signal_map[final_signal_code],
            meta_signal=f"Primary: {signal_map[primary_pred]} | Meta: {'CONFIRMED' if meta_pred==1 else 'REJECTED'}",
            confidence=float(meta_probs[1])
        )
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Model for ticker {request.ticker} not trained yet.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")