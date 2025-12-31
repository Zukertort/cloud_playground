from fastapi import APIRouter, HTTPException, Depends
import numpy as np
import xgboost as xgb
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
        dinput = xgb.DMatrix(features_array)

        primary_prob = primary_model.predict(dinput)[0]
        primary_pred = 1 if primary_prob > 0.5 else 0

        primary_conf = np.array([[primary_prob]])
        meta_features = np.hstack([features_array, primary_conf])

        dmeta = xgb.DMatrix(meta_features)
        meta_prob = meta_model.predict(dmeta)[0]
        meta_pred = 1 if meta_prob > 0.5 else 0

        final_signal_code = 1 if (primary_pred == 1 and meta_pred == 1) else 0

        signal_map = {0: "IGNORE", 1: "BUY"}
        primary_map = {0: "SELL/IGNORE", 1: "BUY"}
        
        return PredictionResponse(
            ticker=request.ticker,
            signal=signal_map[final_signal_code],
            meta_signal=f"Primary: {signal_map[primary_pred]} | Meta: {'CONFIRMED' if meta_pred==1 else 'REJECTED'}",
            confidence=float(meta_prob)
        )
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Model for ticker {request.ticker} not trained yet.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")