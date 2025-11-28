# Market Data Ingestion Pipeline

## Overview
This pipeline handles the ETL (Extract, Transform, Load) process for historical market data. It scrapes the current S&P 500 constituents and ingests daily OHLCV data into a high-performance columnar store.

## Architecture Decisions

### 1. Polars vs Pandas
Used **Polars** for the transformation layer due to its Rust-based query engine and Lazy API.
- **Problem:** Pandas loads all data into RAM (Eager execution), which causes OOM (Out of Memory) errors when processing 500+ high-resolution files on standard hardware.
- **Solution:** Polars optimizes memory usage via zero-copy data sharing and threaded execution, allowing us to process datasets larger than available RAM.

### 2. Storage Format (Parquet + Snappy)
Data is stored as partitioned `.parquet` files with **Snappy** compression.
- **Why Parquet:** Columnar storage allows specific features (e.g., "Close" price) to be queried without scanning the entire dataset (I/O optimization).
- **Why Snappy:** A compression algorithm optimized for high-throughput read speeds, essential for minimizing latency during model training iterations.

### 3. Feature Engineering (Microstructure)
- **Dollar Volume:** Calculated as `Close * Volume`.
- **Theory:** This metric enables downstream transformation from standard Time Bars into **Dollar Bars** (sampling by constant value exchanged). This aligns with Lopez de Prado's findings (*Advances in Financial Machine Learning, 2018*) that sampling by information flow (market activity) rather than chronological time reduces statistical noise (heteroscedasticity) and improves model convergence.

## Usage
Run the ingestion:
```bash
python ingest.py