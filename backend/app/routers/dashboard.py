from fastapi import APIRouter, HTTPException, Depends
from app.dependencies import get_current_user
from app.settings import settings
from app.services.model_loader import global_model_loader
from app.schemas.dashboard import DashboardResponse
import polars as pl
import numpy as np
import os
from app.settings import settings
import xgboost as xgb
from pipeline.sentiment import get_news, get_sentiment

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/{ticker}", response_model=DashboardResponse)
async def get_dashboard_data(ticker: str):
    try:
        base_data_dir = os.path.dirname(settings.MODEL_DIR.rstrip('/'))
        
        feature_path = os.path.join(base_data_dir, "processed", "features", f"{ticker}_features.parquet")
        price_path = os.path.join(base_data_dir, "processed", "labeled", f"{ticker}_db.parquet")

        if not os.path.exists(feature_path) or not os.path.exists(price_path):
            raise FileNotFoundError(f"Data not found for {ticker}")

        df_features = pl.read_parquet(feature_path)
        df_price = pl.read_parquet(price_path)

        history_df = df_price.tail(100)
        
        history = history_df.select([
            pl.col("timestamp").cast(pl.Utf8), 
            pl.col("close")
        ]).to_dicts()

        last_row = df_features.tail(1)
        
        lags = [1, 2, 3, 5, 10]
        feature_cols = ["volatility", "rsi", "frac_diff_04"]
        for lag in lags:
            col_name = f"return_lag_{lag}"
            if col_name in df_features.columns:
                 feature_cols.append(col_name)
        
        features_array = last_row.select(feature_cols).to_numpy()

        models = global_model_loader.get_model(ticker)
        primary_model = models["model"]
        meta_model = models["meta_model"]

        dinput = xgb.DMatrix(features_array)

        primary_prob_val = primary_model.predict(dinput)[0]

        primary_pred = 1 if primary_prob_val > 0.5 else 0

        primary_conf = np.array([[primary_prob_val]])
        meta_features = np.hstack([features_array, primary_conf])

        dmeta = xgb.DMatrix(meta_features)
        meta_prob_val = meta_model.predict(dmeta)[0]
        meta_pred = 1 if meta_prob_val > 0.5 else 0

        final_signal_code = 1 if (primary_pred == 1 and meta_pred == 1) else 0

        conf_value = float(meta_prob_val)
        if np.isnan(conf_value):
            conf_value = 0.0
        
        signal_map = {0: "IGNORE", 1: "BUY"}
        primary_map = {0: "SELL/IGNORE", 1: "BUY"}

        # GENAI integration
        headlines = get_news(ticker)
        score = get_sentiment(headlines, mock=settings.USE_MOCK_SENTIMENT)

        analysis = "Neutral"
        if score > 0.3: analysis = "Positive"
        if score < -0.3: analysis = "Negative"

        return DashboardResponse(
            ticker=ticker,
            current_price=history[-1]["close"],
            signal=signal_map[final_signal_code],
            meta_signal=f"Primary: {primary_map[primary_pred]} | Meta: {'CONFIRMED' if meta_pred == 1 else 'REJECTED'}",
            confidence=conf_value,
            history=history,
            sentiment_score=score,
            sentiment_analysis=analysis,
            news_headlines=headlines[:3]
        )

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Ticker {ticker} not found in database.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DEBUG ERROR: {str(e)}")