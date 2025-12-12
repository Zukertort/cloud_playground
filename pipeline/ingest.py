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
        if len(existing_files) > 10:
            print(f"Loaded {len(existing_files)} tickers from local storage.")
            return existing_files

    print("Local data empty. Scraping S&P 500 constituents...")
    try:
        url = "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/master/data/constituents.csv"

        df = pd.read_csv(url)
        tickers = df['Symbol'].tolist()
        
        tickers = [t.replace('.', '-') for t in tickers]
        
        print(f"Found {len(tickers)} tickers.")
        return tickers
    
    except Exception as e:
        print(f"Scraping failed: {e}")
        print("Activating fallback method: Using Top 20 Liquid Tech Stocks.")
        return [
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", 
            "AMD", "INTC", "QCOM", "CSCO", "NFLX", "ADBE", "TXN", 
            "AVGO", "CRM", "PYPL", "IBM", "ORCL", "MU"
        ]

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

    df_pandas = df_pandas.reset_index()

    df = pl.from_pandas(df_pandas)
    
    if len(df.columns) == 6:
        df.columns = ["date", "open", "high", "low", "close", "volume"]
    else:
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