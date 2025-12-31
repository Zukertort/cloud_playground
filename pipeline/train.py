import polars as pl
import xgboost as xgb
from sklearn.metrics import precision_score
import numpy as np
import os
from tqdm import tqdm
import mlflow

FEATURES_DIR = "./data/processed/features"
MODEL_DIR = "./data/models"

def get_available_tickers():
    if not os.path.exists(FEATURES_DIR):
        return []
    files = [f for f in os.listdir(FEATURES_DIR) if f.endswith("_features.parquet")]
    return [f.replace("_features.parquet", "") for f in files]

def train_meta_model(df_clean, primary_model, feature_cols):
    """
    Trains using Core XGBoost API.
    """
    X = df_clean.select(feature_cols).to_numpy()
    y_true = df_clean.select("target").to_numpy().ravel()
    
    dmatrix = xgb.DMatrix(X)
    primary_probs = primary_model.predict(dmatrix)
    
    primary_preds = (primary_probs > 0.5).astype(int)
    meta_target = (primary_preds == y_true).astype(int)
    
    primary_conf = primary_probs.reshape(-1, 1)
    X_meta = np.hstack([X, primary_conf])
    
    dmeta = xgb.DMatrix(X_meta, label=meta_target)
    params = {
        "objective": "binary:logistic",
        "max_depth": 3,
        "eta": 0.1,
        "eval_metric": "logloss",
        "nthread": 1
    }
    meta_model = xgb.train(params, dmeta, num_boost_round=100)
    
    return meta_model

def train_ticker(ticker, save=True):
    path = f"{FEATURES_DIR}/{ticker}_features.parquet"
    mlflow.set_experiment(f"Alpha_{ticker}")
    
    try:
        df = pl.read_parquet(path)

        required_cols = ["volatility", "rsi", "label"]
        for col in required_cols:
            if col not in df.columns: return None

        lags = [1, 2, 3, 5, 10]
        feature_cols = ["volatility", "rsi", "frac_diff_04"]
        for lag in lags:
            if f"return_lag_{lag}" in df.columns: feature_cols.append(f"return_lag_{lag}")
        
        df_clean = (
            df.filter(pl.col("label") != 0)
              .drop_nulls()
              .with_columns(
                  pl.when(pl.col("label") == -1).then(0)
                  .otherwise(1).alias("target")
              )
        )
        
        if df_clean.height < 50: return None


        split_idx = int(df_clean.height * 0.80)
        train = df_clean.slice(0, split_idx)
        test = df_clean.slice(split_idx, df_clean.height - split_idx)
        
        X_train = train.select(feature_cols).to_numpy()
        y_train = train.select("target").to_numpy().ravel()
        X_test = test.select(feature_cols).to_numpy()
        y_test = test.select("target").to_numpy().ravel()
        
        dtrain = xgb.DMatrix(X_train, label=y_train)
        params = {
            "objective": "binary:logistic",
            "max_depth": 3,
            "eta": 0.1,
            "eval_metric": "logloss",
            "nthread": 1
        }

        with mlflow.start_run(nested=True):
            mlflow.log_param("model_type", "XGBoost")
            mlflow.log_param("n_estimators", 100)
            mlflow.log_param("max_depth", 3)
            mlflow.log_param("features", feature_cols)

        primary_model = xgb.train(params, dtrain, num_boost_round=100)

        meta_model = train_meta_model(train, primary_model, feature_cols)
        
        if save:
            if not os.path.exists(MODEL_DIR): os.makedirs(MODEL_DIR)
            primary_model.save_model(f"{MODEL_DIR}/{ticker}_primary.json")
            meta_model.save_model(f"{MODEL_DIR}/{ticker}_meta.json")

        dtest = xgb.DMatrix(X_test)
        primary_test_probs = primary_model.predict(dtest)
        
        test_conf = primary_test_probs.reshape(-1, 1)
        X_test_meta = np.hstack([X_test, test_conf])
        
        dmeta_test = xgb.DMatrix(X_test_meta)
        meta_probs = meta_model.predict(dmeta_test)

        primary_preds = (primary_test_probs > 0.5).astype(int)
        meta_preds = (meta_probs > 0.5).astype(int)
        
        final_signal = (primary_preds == 1) & (meta_preds == 1)

        precision = precision_score(y_test, final_signal, pos_label=1, zero_division=0)

        if np.sum(final_signal) == 0: return 0.0

        mlflow.log_metric("precision", float(precision))

        return precision
        

    except Exception as e:
        print(f"Error training {ticker}: {str(e)}")
        return None

def main():
    tickers = get_available_tickers()

    target_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
    run_list = [t for t in tickers if t in target_tickers]
    if not run_list: run_list = tickers[:5]

    print(f"--- TRAINING ON {len(run_list)} TICKERS ---")
    scores = []
    for ticker in tqdm(run_list):
        score = train_ticker(ticker)
        if score is not None:
            scores.append(score)
            
    if scores:
        print(f"\nAVERAGE PRECISION: {sum(scores)/len(scores):.2%}")

if __name__ == "__main__":
    main()