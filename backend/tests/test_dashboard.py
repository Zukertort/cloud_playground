import unittest
from fastapi.testclient import TestClient
from app.main import app
import polars as pl

dummy_df = pl.DataFrame({
    "ticker": ["AAPL", "MSFT", "GOOG", "AMZN"],
    "date": ["2022-01-01", "2022-01-02", "2022-01-03", "2022-01-04"],
    "close": [100, 200, 300, 400]
})

client = TestClient(app)