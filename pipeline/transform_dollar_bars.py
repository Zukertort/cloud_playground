import polars as pl
import os
from tqdm import tqdm

RAW_DIR = "./data/raw"
PROCESSED_DIR = "./data/processed/dollar_bars"
THRESHOLD = 5_000_000_000  # $5B (Adjustable based on asset)

def ensure_dir():
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)

def process_ticker(ticker_file):
    # Lazy Scan the Parquet (Memory Efficient)
    q = pl.scan_parquet(ticker_file)
    
    # Calculate Cumulative Dollar Volume
    # We need to realize the dataframe here to iterate, 
    # but Polars is fast enough for single files.
    df = q.collect()
    
    if df.height == 0:
        return

    # The Logic: Grouping by Threshold
    # We calculate a cumulative sum of dollar volume.
    # We divide by threshold to get a "Group ID".
    # Floor() gives us the integer bucket.
    
    df = df.with_columns(
        (pl.col("dollar_volume").cum_sum() / THRESHOLD).floor().alias("bar_id")
    )
    
    # Aggregation (Create the new bars)
    dollar_bars = (
        df.group_by("bar_id")
        .agg([
            pl.col("date").first().alias("timestamp"),
            pl.col("open").first().alias("open"),
            pl.col("high").max().alias("high"),
            pl.col("low").min().alias("low"),
            pl.col("close").last().alias("close"),
            pl.col("volume").sum().alias("volume"),
            pl.col("dollar_volume").sum().alias("dollar_volume")
        ])
        .sort("timestamp")
    )
    
    # Save
    ticker_name = os.path.basename(ticker_file).replace(".parquet", "")
    save_path = f"{PROCESSED_DIR}/{ticker_name}_db.parquet"
    dollar_bars.write_parquet(save_path, compression="snappy")

def main():
    ensure_dir()
    files = [os.path.join(RAW_DIR, f) for f in os.listdir(RAW_DIR) if f.endswith(".parquet")]
    
    print(f"Transforming {len(files)} tickers into Dollar Bars (Threshold: ${THRESHOLD:,.0f})...")
    
    for f in tqdm(files):
        try:
            process_ticker(f)
        except Exception as e:
            print(f"Error processing {f}: {e}")

if __name__ == "__main__":
    main()