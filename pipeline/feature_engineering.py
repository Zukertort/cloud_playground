import polars as pl
import os
import functools
from tqdm import tqdm

# We will move this to utils.py later, but for now define or import it
# from utils import time_execution 

LABELED_DIR = "./data/processed/labeled"
FEATURES_DIR = "./data/processed/features"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def calculate_rsi(expr, period=14):
    """
    Polars Expression for RSI.
    Input: pl.col("close")
    Output: RSI values (0-100)
    """
    delta = expr.diff()
    # Up moves: positive delta, clipped at 0
    up = delta.clip(lower_bound=0)
    # Down moves: negative delta, clipped at 0, absolute value
    down = delta.clip(upper_bound=0).abs()

    # Exponential Weighted Moving Average
    roll_up = up.ewm_mean(span=period, adjust=False)
    roll_down = down.ewm_mean(span=period, adjust=False)

    rs = roll_up / roll_down
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi.alias("rsi")

def process_ticker(ticker):
    input_path = f"{LABELED_DIR}/{ticker}_db.parquet"
    if not os.path.exists(input_path):
        print(f"⚠️ Missing {ticker}")
        return

    df = pl.read_parquet(input_path)

    # 1. Base Features (Returns & RSI)
    # We chain .with_columns to ensure "log_return" is available for lags later
    df = df.with_columns([
        (pl.col("close") / pl.col("close").shift(1)).log().alias("log_return"),
        calculate_rsi(pl.col("close"), period=14)
    ])

    # 2. Lags (The Loop)
    # We can add multiple columns at once
    lags = [1, 2, 3, 5, 10]
    lag_expressions = [
        pl.col("log_return").shift(lag).alias(f"return_lag_{lag}") 
        for lag in lags
    ]
    df = df.with_columns(lag_expressions)

    # 3. Save
    output_path = f"{FEATURES_DIR}/{ticker}_features.parquet"
    df.write_parquet(output_path)

def main():
    ensure_dir(FEATURES_DIR)
    # Get all files from labeled dir
    files = [f.replace("_db.parquet", "") for f in os.listdir(LABELED_DIR) if f.endswith("_db.parquet")]
    
    print(f"Engineering features for {len(files)} tickers...")
    for ticker in tqdm(files):
        try:
            process_ticker(ticker)
        except Exception as e:
            print(f"Error {ticker}: {e}")

if __name__ == "__main__":
    main()