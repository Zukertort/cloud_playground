import pytest
import polars as pl
import polars.testing as pl_test
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from feature_engineering import calculate_rsi

def test_rsi_flat_line():
    """
    If price is constant, RSI should eventually settle at 50 (Neutral).
    """
    df = pl.DataFrame({
        "close": [100.0] * 50
    })
    
    result = df.select(
        calculate_rsi(pl.col("close"), period=14).alias("rsi")
    )
    
    last_rsi = result["rsi"].tail(1).item()
    
    assert abs(last_rsi - 50.0) < 0.1 or (last_rsi != last_rsi)

def test_rsi_uptrend():
    """
    If price goes up every single day, RSI should be very high (near 100).
    """
    prices = [100.0 + i for i in range(50)]
    df = pl.DataFrame({"close": prices})
    
    result = df.select(
        calculate_rsi(pl.col("close"), period=14).alias("rsi")
    )
    
    last_rsi = result["rsi"].tail(1).item()
    
    print(f"Uptrend RSI: {last_rsi}")
    assert last_rsi > 70.0

def test_rsi_downtrend():
    """
    If price goes down monotonically, RSI should be Oversold (<30).
    """
    prices = [100.0 - i for i in range(30)]
    df = pl.DataFrame({"close": prices})
    
    result = df.select(
        calculate_rsi(pl.col("close"), period=14).alias("rsi")
    )
    
    last_rsi = result["rsi"].tail(1).item()
    
    # Should be oversold (< 30)
    print(f"Downtrend RSI: {last_rsi}")
    assert last_rsi < 30.0