import polars as pl
import xgboost as xgb
from sklearn.metrics import precision_score
import numpy as np
import os
import joblib
from tqdm import tqdm

# NOW WE READ FROM FEATURES DIRECTORY
FEATURES_DIR = "./data/processed/features"
MODEL_DIR = "./data/models"
TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]

def train_ticker(ticker, save=True):
    path = f"{FEATURES_DIR}/{ticker}_features.parquet"
    if not os.path.exists(path):
        print(f"⚠️  Missing features for {ticker}")
        return None
    
    df = pl.read_parquet(path)
    
    # Define Feature Columns (Must match what we created in feature_engineering.py)
    # Volatility came from labeling, RSI/Lags came from feature_engineering
    feature_cols = ["volatility", "rsi"] 
    lags = [1, 2, 3, 5, 10]
    for lag in lags:
        feature_cols.append(f"return_lag_{lag}")

    # Clean & Target
    df_clean = (
        df.filter(pl.col("label") != 0)
          .drop_nulls()
          .with_columns(
              pl.when(pl.col("label") == -1).then(0)
              .otherwise(1)
              .alias("target")
          )
    )
    
    if df_clean.height < 50:
        return None

    # Split
    split_idx = int(df_clean.height * 0.80)
    train = df_clean.slice(0, split_idx)
    test = df_clean.slice(split_idx, df_clean.height - split_idx)
    
    # Numpy
    X_train = train.select(feature_cols).to_numpy()
    y_train = train.select("target").to_numpy().ravel()
    X_test = test.select(feature_cols).to_numpy()
    y_test = test.select("target").to_numpy().ravel()
    
    # Train
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=3,
        learning_rate=0.1,
        eval_metric='logloss',
        verbosity=0
    )
    model.fit(X_train, y_train)
    
    # Save
    if save:
        if not os.path.exists(MODEL_DIR): os.makedirs(MODEL_DIR)
        model.save_model(f"{MODEL_DIR}/{ticker}_xgb.json")

    # Evaluate
    preds = model.predict(X_test)
    if np.sum(preds) == 0: return 0.0
    return precision_score(y_test, preds, pos_label=1, zero_division=0)

def main():
    print(f"--- TRAINING ON {len(TICKERS)} TECH GIANTS ---")
    scores = []
    for ticker in tqdm(TICKERS):
        score = train_ticker(ticker)
        if score is not None:
            scores.append(score)
            
    if scores:
        print(f"\n🏆 AVERAGE PRECISION: {sum(scores)/len(scores):.2%}")

if __name__ == "__main__":
    main()