import yfinance as yf
import polars as pl
import pandas as pd
import requests
import os
from datetime import datetime
from tqdm import tqdm
from io import StringIO
from utils import time_execution, retry

def get_sp500_tickers() -> list[str]:
    print("Scraping S&P 500 constituents...")
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    
    #Add a browser User-Agent
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    tables = pd.read_html(StringIO(r.text))

    target_table = None
    for t in tables:
        # We look for a table that has 'Symbol' and 'Security' columns
        if 'Symbol' in t.columns and 'Security' in t.columns:
            target_table = t
            break
            
    if target_table is None:
        raise ValueError("Could not find the S&P 500 table on Wikipedia.")
        
    tickers = target_table['Symbol'].tolist()
    
    # Clean ticker names (YF uses '-' instead of '.' for BRK.B)
    tickers = [t.replace('.', '-') for t in tickers]
    
    print(f"Found {len(tickers)} tickers.")
    return tickers

TICKERS = get_sp500_tickers()
DATA_DIR = "./data/raw"

def ensure_directories():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
@retry(retries=3, delay=2)
def fetch_data(ticker: str) -> pl.DataFrame:

    try:
        # Download using yfinance
        df_pandas = yf.download(ticker, period="2y", interval="1h", progress=False, auto_adjust=True)
    except Exception:
        return None
    
    if df_pandas.empty:
        return None

    # Reset index to make Date a column
    df_pandas = df_pandas.reset_index()

    # Convert to Polars
    df = pl.from_pandas(df_pandas)
    
    # Clean Column Names
    if len(df.columns) == 6:
        df.columns = ["date", "open", "high", "low", "close", "volume"]
    else:
        # Handle edge cases (sometimes 'Adj Close' is there)
        # For this MVP, we just take the first 6
        df = df.select(df.columns[:6])
        df.columns = ["date", "open", "high", "low", "close", "volume"]
    
    # Add Ticker Column
    df = df.with_columns(pl.lit(ticker).alias("ticker"))
    
    # Add Dollar Volume
    df = df.with_columns(
        (pl.col("close") * pl.col("volume")).alias("dollar_volume")
    )

    return df

def save_to_parquet(df: pl.DataFrame, ticker: str):
    file_path = f"{DATA_DIR}/{ticker}.parquet"
    df.write_parquet(file_path, compression="snappy")

@time_execution
def main():
    ensure_directories()
    
    success_count = 0
    
    for ticker in tqdm(TICKERS, desc="Ingesting Market Data"):
        try:
            df = fetch_data(ticker)
            if df is not None:
                save_to_parquet(df, ticker)
                success_count += 1
        except Exception as e:
            pass

    print(f"\nPipeline Finished. Successfully ingested {success_count}/{len(TICKERS)} tickers.")

if __name__ == "__main__":
    main()