import polars as pl

# Paths
raw_path = "./data/raw/AAPL.parquet"
processed_path = "./data/processed/dollar_bars/AAPL_db.parquet"

# Load
df_raw = pl.read_parquet(raw_path)
df_dollar = pl.read_parquet(processed_path)

print(f"--- AAPL ANALYSIS ---")
print(f"Raw Time Bars (Daily): {df_raw.height} rows")
print(f"Dollar Bars ($10M):    {df_dollar.height} rows")
print(f"Reduction Factor:      {df_raw.height / df_dollar.height:.2f}x")

# Check the first few rows to see if prices look sane
print("\nFirst 5 Dollar Bars:")
print(df_dollar.head(5))