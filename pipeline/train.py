import polars as pl
import xgboost as xgb
from sklearn.metrics import precision_score
import numpy as np
import os
from tqdm import tqdm
import joblib

# We look for data in the LABELED folder (output of labeling.py)
LABELED_DIR = "./data/processed/labeled"
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]

def train_ticker(ticker, save=True):
    """
    Trains a model for a specific ticker and returns the UP Precision.
    """
    # Load Data
    path = f"{LABELED_DIR}/{ticker}_db.parquet"
    if not os.path.exists(path):
        print(f"⚠️  Missing data for {ticker}")
        return None
    
    df = pl.read_parquet(path)
    
    # Feature Engineering (Lags + Volatility)
    # We recreate features here for each file
    df = df.with_columns(
        (pl.col("close") / pl.col("close").shift(1)).log().alias("log_return")
    )
    
    lags = [1, 2, 3, 5, 10]
    feature_cols = ["volatility"] # Volatility already exists from labeling.py
    for lag in lags:
        feat_name = f"return_lag_{lag}"
        df = df.with_columns(
            pl.col("log_return").shift(lag).alias(feat_name)
        )
        feature_cols.append(feat_name)
        
    # Clean & Target
    # Drop 0s (Timeouts) and NaNs
    df_clean = (
        df.filter(pl.col("label") != 0)
          .drop_nulls()
          .with_columns(
              pl.when(pl.col("label") == -1).then(0) # Down -> 0
              .otherwise(1)                          # Up -> 1
              .alias("target")
          )
    )
    
    if df_clean.height < 50:
        print(f"⚠️  Not enough samples for {ticker}")
        return None

    # Time Series Split (80/20)
    split_idx = int(df_clean.height * 0.80)
    train = df_clean.slice(0, split_idx)
    test = df_clean.slice(split_idx, df_clean.height - split_idx)
    
    # Numpy Conversion
    X_train = train.select(feature_cols).to_numpy()
    y_train = train.select("target").to_numpy().ravel()
    X_test = test.select(feature_cols).to_numpy()
    y_test = test.select("target").to_numpy().ravel()
    
    # Train XGBoost
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.1,
        eval_metric='logloss',
        verbosity=0
    )
    model.fit(X_train, y_train)

    # Save Model
    if save:
        model_dir = "./data/models"
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        
        # Save the Model (JSON is smaller/faster for XGBoost)
        model.save_model(f"{model_dir}/{ticker}_xgb.json")
        print(f"   💾 Saved model to {model_dir}/{ticker}_xgb.json")
    
    # Evaluate
    preds = model.predict(X_test)
    
    # Check if we predicted ANY 'Up' moves
    if np.sum(preds) == 0:
        return 0.0 # Model was too scared to trade
        
    prec = precision_score(y_test, preds, pos_label=1, zero_division=0)
    return prec

def main():
    print(f"--- TRAINING ON {len(TICKERS)} TECH GIANTS ---")
    
    scores = []
    
    for ticker in TICKERS:
        score = train_ticker(ticker)
        if score is not None:
            print(f"{ticker}: {score:.2%} Precision (Long)")
            scores.append(score)
            
    if scores:
        avg_precision = sum(scores) / len(scores)
        print(f"\n🏆 AVERAGE LONG PRECISION: {avg_precision:.2%}")
        
        if avg_precision > 0.53:
            print("✅ RESULT: We have Alpha.")
        else:
            print("❌ RESULT: Noise / Random Walk.")
    else:
        print("No models trained successfully.")

if __name__ == "__main__":
    main()