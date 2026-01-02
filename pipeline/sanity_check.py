import polars as pl
import numpy as np
import os
import sys

try:
    import quant_engine
except ImportError:
    print("Critical: quant_engine module not found. Check LD_PRELOAD or installation.")
    sys.exit(1)

LABELED_DIR = "./data/processed/labeled"

def check_ticker(ticker):
    path = f"{LABELED_DIR}/{ticker}_db.parquet"
    if not os.path.exists(path):
        print(f"{ticker} file not found.")
        return

    df = pl.read_parquet(path)
    prices = df["close"].to_numpy().astype(np.float64)
    
    print(f"\n--- Checking {ticker} ---")
    print(f"Input Rows: {len(prices)}")

    try:
        res = quant_engine.fractional_diff(prices, 0.4, 1e-3)
        print(f"Output Rows: {len(res)}")
        
        # Check for Data Quality
        nans = np.isnan(res).sum()
        valid = len(res) - nans
        print(f"NaNs (Padding): {nans}")
        print(f"Valid Values:   {valid}")
        
        if valid > 0:
            print(f"SUCCESS. Sample: {res[-5:]}")
        else:
            print(f"FAILURE. All values are NaN. Window might be too large.")
            
        if len(res) == 0:
            print("CRITICAL FAILURE. Returned length 0.")

    except Exception as e:
        print(f"CRASH: {e}")

if __name__ == "__main__":
    # Test a Long History (Should work)
    check_ticker("AAPL")
    
    # Test a Short History (Likely DVA or GL if you have them locally)
    check_ticker("DVA")