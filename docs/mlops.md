# MLOps Architecture & Strategy

## Overview
This platform implements a **Level 2 MLOps** maturity model (Automated Pipeline), ensuring that trading signals are generated from the freshest data without manual intervention.

## 1. The Continuous Training (CT) Pipeline
The system utilizes an Event-Driven architecture triggered by a Background Scheduler (APScheduler).

### Workflow
1.  **Incremental Ingestion:** The pipeline checks the latest timestamp in the Parquet Data Lake and downloads only missing delta frames from the provider.
2.  **Vectorized Transformation:** Raw time-bars are converted to **Dollar Bars** ($5B threshold) to recover stationarity.
3.  **Feature Store:** Features (RSI, Volatility, FracDiff) are computed once and stored in Parquet format, decoupling training from engineering.
4.  **Hierarchical Training:**
    *   **Primary Model:** Predicts direction (Buy/Sell).
    *   **Meta-Model:** Predicts the *probability* of the Primary Model being correct.

## 2. Infrastructure as Code (IaC)
*   **Containerization:** The entire stack (C++ Engine + Python API) is defined in `Dockerfile`, ensuring 100% reproducibility across dev and prod environments.
*   **Hybrid Runtime:** We utilize a custom-built C++23 extension (`quant_engine`) linked via PyBind11, running inside a standard Debian Python container.

## 3. Model Serving Strategy
We utilize a **Singleton Model Loader** pattern.
*   **Cold Start:** On container boot, the system checks for existing artifacts. If missing, it triggers a full retraining cycle.
*   **In-Memory Caching:** Models are loaded into RAM (`xgb.Booster`) to ensure sub-millisecond inference latency (avoiding disk I/O per request).

## 4. Quality Gates
*   **Unit Tests:** Mathematical indicators (RSI) are verified via `pytest`.
*   **Integration Tests:** The pipeline is validated end-to-end via GitHub Actions.