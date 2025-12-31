import polars as pl
import matplotlib.pyplot as plt
import os

DATA_PATH = "./data/processed/features/AAPL_features.parquet"
OUTPUT_IMG = "../docs/images/frac_diff_analysis.png"

def main():
    if not os.path.exists(DATA_PATH):
        print("Data not found.")
        return

    df = pl.read_parquet(DATA_PATH)
  
    print(f"Total Rows: {df.height}")
    null_count = df["frac_diff_04"].null_count()
    print(f"FracDiff Nulls: {null_count} ({null_count/df.height:.1%} of data)")

    valid_data = df.drop_nulls(subset=["frac_diff_04"])
    if valid_data.height > 0:
        print("First 5 Valid Values:")
        print(valid_data["frac_diff_04"].head(5))
        print("Last 5 Valid Values:")
        print(valid_data["frac_diff_04"].tail(5))
    else:
        print("CRITICAL: FracDiff column is empty/all-null.")
    
    dates = df["timestamp"].to_list()
    close = df["close"].to_numpy()
    frac = df["frac_diff_04"].to_numpy()
    rets = df["log_return"].to_numpy()

    fig, axes = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    
    axes[0].plot(dates, close, color='blue', label='Close Price')
    axes[0].set_title('Raw Price (Non-Stationary)')
    axes[0].legend(loc="upper left")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(dates, frac, color='purple', label='Frac Diff (d=0.4)')
    axes[1].set_title('Fractional Differentiation (Stationary + Memory)')
    axes[1].legend(loc="upper left")
    axes[1].grid(True, alpha=0.3)

    axes[2].plot(dates, rets, color='gray', label='Log Returns', alpha=0.7)
    axes[2].set_title('Log Returns (Stationary + No Memory)')
    axes[2].legend(loc="upper left")
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    
    os.makedirs(os.path.dirname(OUTPUT_IMG), exist_ok=True)
    plt.savefig(OUTPUT_IMG)
    print(f"Analysis saved to {OUTPUT_IMG}")

if __name__ == "__main__":
    main()