import pytest
import polars as pl
import polars.testing as pl_test
import sys
import os

# Pipeline directory to path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from feature_engineering import calculate_rsi

def test_rsi_flat_line():
    """
    If price never changes, RSI should be NaN or stable (depending on implementation).
    """
    df = pl.DataFrame({
        "close": [100.0] * 20
    })
    
    result = df.select(
        calculate_rsi(pl.col("close"), period=14).alias("rsi")
    )
    
    last_rsi = result["rsi"].tail(1).item()
    
    assert last_rsi == 50.0 or last_rsi is None or (last_rsi != last_rsi)

def test_rsi_uptrend():
    """
    If price goes up every single day, RSI should be very high (near 100).
    """
    prices = [100.0 + i for i in range(30)]
    df = pl.DataFrame({"close": prices})
    
    result = df.select(
        calculate_rsi(pl.col("close"), period=14).alias("rsi")
    )
    
    last_rsi = result["rsi"].tail(1).item()
    
    print(f"Uptrend RSI: {last_rsi}")
    assert last_rsi > 90.0

def test_rsi_downtrend():
    """
    If price crashes, RSI should be near 0.
    """
    prices = [100.0 - i for i in range(30)]
    df = pl.DataFrame({"close": prices})
    
    result = df.select(
        calculate_rsi(pl.col("close"), period=14).alias("rsi")
    )
    
    last_rsi = result["rsi"].tail(1).item()
    
    # Should be oversold (< 30)
    print(f"Downtrend RSI: {last_rsi}")
    assert last_rsi < 10.0