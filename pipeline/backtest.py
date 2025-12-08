import polars as pl
import numpy as np
import xgboost as xgb
import os
import matplotlib.pyplot as plt

# Config
FEATURES_DIR = "./data/processed/features"
LABELED_DIR = "./data/processed/labeled" # Contains 'close' prices and dates
MODEL_DIR = "./data/models"
TICKER = "AAPL" # Test

def load_models(ticker):
    primary = xgb.XGBClassifier()
    primary.load_model(f"{MODEL_DIR}/{ticker}_primary.json")
    
    meta = xgb.XGBClassifier()
    meta.load_model(f"{MODEL_DIR}/{ticker}_meta.json")
    return primary, meta

def run_backtest(ticker):
    print(f"--- Backtesting {ticker} ---")
    
    df_features = pl.read_parquet(f"{FEATURES_DIR}/{ticker}_features.parquet")
    df_price = pl.read_parquet(f"{LABELED_DIR}/{ticker}_db.parquet")
    
    min_len = min(df_features.height, df_price.height)
    df_features = df_features.slice(0, min_len)
    df_price = df_price.slice(0, min_len)
    
    feature_cols = ["volatility", "rsi"] + [col for col in df_features.columns if "return_lag_" in col]
    X = df_features.select(feature_cols).to_numpy()
    
    primary_model, meta_model = load_models(ticker)

    primary_preds = primary_model.predict(X)
    primary_probs = primary_model.predict_proba(X)
    
    primary_conf = np.max(primary_probs, axis=1).reshape(-1, 1)
    X_meta = np.hstack([X, primary_conf])
    
    meta_preds = meta_model.predict(X_meta)
    
    signal = (primary_preds == 1) & (meta_preds == 1)
    
    df_res = df_price.with_columns(
        (pl.col("close").shift(-1) / pl.col("close") - 1).alias("market_return")
    )
    
    df_res = df_res.with_columns(pl.Series(name="signal", values=signal))
    
    df_res = df_res.with_columns(
        (pl.col("market_return") * pl.col("signal")).alias("strategy_return")
    )
    
    df_res = df_res.with_columns([
        (1 + pl.col("market_return")).cum_prod().alias("cum_market"),
        (1 + pl.col("strategy_return")).cum_prod().alias("cum_strategy")
    ]).drop_nulls()
    
    final_market = df_res["cum_market"].tail(1).item()
    final_strategy = df_res["cum_strategy"].tail(1).item()
    
    risk_free = 0.04 / (252*7)
    excess_ret = df_res["strategy_return"] - risk_free
    sharpe = (excess_ret.mean() / excess_ret.std()) * np.sqrt(252 * 7)
    
    print(f"Buy & Hold Return: {(final_market - 1):.2%}")
    print(f"Strategy Return:   {(final_strategy - 1):.2%}")
    print(f"Sharpe Ratio:      {sharpe:.2f}")

    plt.figure(figsize=(12, 6))
    
    dates = df_res["timestamp"].to_list()
    equity_market = df_res["cum_market"].to_list()
    equity_strategy = df_res["cum_strategy"].to_list()
    
    plt.plot(dates, equity_market, label="Buy & Hold (Benchmark)", alpha=0.6)
    plt.plot(dates, equity_strategy, label="Meta-Labeling Strategy", color="green", linewidth=2)
    
    plt.title(f"Backtest Result: {ticker} (Sharpe: {sharpe:.2f})")
    plt.ylabel("Cumulative Return")
    plt.xlabel("Date")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    output_img = f"./docs/images/{ticker}_backtest.png"
    if not os.path.exists("./docs/images"): os.makedirs("./docs/images")
    
    plt.savefig(output_img)
    print(f"Chart saved to {output_img}")
    
    # Optional: plt.show() if running locally with UI
    
    return df_res

if __name__ == "__main__":
    df = run_backtest(TICKER)