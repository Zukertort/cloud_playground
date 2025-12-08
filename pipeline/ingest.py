import yfinance as yf
import polars as pl
import pandas as pd
import requests
import os
from datetime import datetime
from tqdm import tqdm
from io import StringIO
from utils import time_execution, retry

DATA_DIR = "./data/raw"

def get_sp500_tickers() -> list[str]:
    if os.path.exists(DATA_DIR):
        existing_files = [f.replace(".parquet", "") for f in os.listdir(DATA_DIR) if f.endswith(".parquet")]
        if len(existing_files) > 400: # If we have data, use it
            print(f"Loaded {len(existing_files)} tickers from local storage.")
            return existing_files

    # 2. Fallback to Wikipedia (Only if local storage is empty)
    print("Local data empty. Scraping S&P 500 constituents...")
    try:
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        r = requests.get(url, headers=headers)
        tables = pd.read_html(StringIO(r.text))

        target_table = None
        for t in tables:
            if 'Symbol' in t.columns and 'Security' in t.columns:
                target_table = t
                break
                
        if target_table is None:
            raise ValueError("Could not find the S&P 500 table on Wikipedia.")
            
        tickers = target_table['Symbol'].tolist()
        
        tickers = [t.replace('.', '-') for t in tickers]
        
        print(f"Found {len(tickers)} tickers.")
        return tickers
    
    except Exception as e:
        print(f"Scraping failed: {e}")
        return []

TICKERS = get_sp500_tickers()

def ensure_directories():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def get_latest_timestamp(ticker: str):
    file_path = f"{DATA_DIR}/{ticker}.parquet"
    if not os.path.exists(file_path):
        return None
    
    df = pl.read_parquet(file_path)
    return df["date"].max()

@retry(retries=3, delay=2)
def fetch_data(ticker: str, start_date: str | None = None) -> pl.DataFrame:
    print(f"Fetching {ticker}..." + (f" from {start_date}" if start_date else " (Full History)"))

    try:
        if start_date:
            start_str = start_date.strftime('%Y-%m-%d') if hasattr(start_date, 'strftime') else start_date
            df_pandas = yf.download(ticker, start=start_str, interval="1h", progress=False, auto_adjust=True)
        else:
            df_pandas = yf.download(ticker, period="2y", interval="1h", progress=False, auto_adjust=True)

    except Exception:
        return None
    
    if df_pandas.empty:
        return None

    # Reset index to make Date a column
    df_pandas = df_pandas.reset_index()

    df = pl.from_pandas(df_pandas)
    
    if len(df.columns) == 6:
        df.columns = ["date", "open", "high", "low", "close", "volume"]
    else:
        # MVP just take the first 6
        df = df.select(df.columns[:6])
        df.columns = ["date", "open", "high", "low", "close", "volume"]
    
    df = df.with_columns(pl.lit(ticker).alias("ticker"))
    
    df = df.with_columns(
        (pl.col("close") * pl.col("volume")).alias("dollar_volume")
    )

    return df

def save_to_parquet(df: pl.DataFrame, ticker: str):
    file_path = f"{DATA_DIR}/{ticker}.parquet"
    df.write_parquet(file_path, compression="snappy")

def update_ticker(ticker: str):
    last_date = get_latest_timestamp(ticker)
    new_df = fetch_data(ticker, start_date=last_date)

    if new_df is None or new_df.height == 0:
        return
    
    if last_date is None:
        final_df = new_df
    else:
        print(f"   Merging {new_df.height} new rows...")
        old_df = pl.read_parquet(f"{DATA_DIR}/{ticker}.parquet")
        final_df = (
            old_df.vstack(new_df)
            .unique(subset=["date"], keep="last")
            .sort(by="date")
        )

    save_to_parquet(final_df, ticker)

@time_execution
def main():
    ensure_directories()
    
    success_count = 0
    
    for ticker in tqdm(TICKERS, desc="Ingesting Market Data"):
        try:
            df = update_ticker(ticker)
            
        except Exception as e:
            pass

    print(f"\nPipeline Finished.")

if __name__ == "__main__":
    main()