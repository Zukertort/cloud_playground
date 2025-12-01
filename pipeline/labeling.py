import polars as pl
import numpy as np
import os
import tqdm

def get_volatility(df, span=100):
    # Compute daily volatility using Exponential Moving Average
    # In Polars, we use ewm_std (Exponentially Weighted Moving Standard Deviation)
    return df.select(
        pl.col("close").pct_change().ewm_std(span=span).alias("volatility")
    )

def triple_barrier_method(df, profit_take=2.0, stop_loss=2.0, horizon=10):
    """
    labels: 1 (Profit), -1 (Loss), 0 (Time-out)
    """
    # Calculate Barriers based on dynamic volatility
    # This is dynamic: When market is crazy, barriers widen.
    df = df.with_columns(
        pl.col("close").pct_change().ewm_std(span=20).fill_null(0.01).alias("volatility")
    )

    # Creating the 'Future' columns to peek ahead
    # In a real engine, we iterate events. For vectorization, we shift.
    # We check the next 'horizon' bars.
    
    # Simple Vectorized approach for MVP:
    # Look at return 'horizon' bars into the future
    future_return = (pl.col("close").shift(-horizon) / pl.col("close")) - 1
    
    # Dynamic Thresholds
    upper = pl.col("volatility") * profit_take
    lower = -pl.col("volatility") * stop_loss
    
    labels = (
        pl.when(future_return > upper).then(1)
        .when(future_return < lower).then(-1)
        .otherwise(0)
        .alias("label")
    )
    
    return df.with_columns(labels)

def main():
    # Process all parquet files in dollar_bars folder
    files = [f for f in os.listdir("./data/processed/dollar_bars") if f.endswith("_db.parquet")]
    
    print(f"Labeling {len(files)} tickers...")
    
    for f in tqdm.tqdm(files):
        try:
            input_path = os.path.join("./data/processed/dollar_bars", f)
            df = pl.read_parquet(input_path)
            
            labeled_df = triple_barrier_method(df)
            
            # Save to new folder "labeled"
            output_dir = "./data/processed/labeled"
            if not os.path.exists(output_dir): os.makedirs(output_dir)
            
            labeled_df.write_parquet(os.path.join(output_dir, f))
        except Exception as e:
            print(f"Error labeling {f}: {e}")

if __name__ == "__main__":
    main()