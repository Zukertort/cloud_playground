import polars as pl
import glob

# Read all parquet files at once (Polars magic)
files = glob.glob("./data/raw/*.parquet")
if not files:
    print("No data found!")
    exit()

q = (
    pl.scan_parquet("./data/raw/*.parquet")
    .group_by("ticker")
    .agg([
        pl.len(),
        pl.col("date").min().alias("start_date"),
        pl.col("date").max().alias("end_date"),
        pl.col("close").mean().alias("avg_price")
    ])
)

print(q.collect())