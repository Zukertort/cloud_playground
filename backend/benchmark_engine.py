import quant_engine
import numpy as np
import time

def run_benchmark(size):
    print(f"\n--- Benchmarking Size: {size:,} elements ---")
    
    data = np.random.rand(size).astype(np.float64)
    window = 100
    
    quant_engine.calculate_volatility(data[:1000], window)

    start = time.perf_counter()
    result = quant_engine.calculate_volatility(data, window) 
    end = time.perf_counter()
    
    duration_ms = (end - start) * 1000
    print(f"Calculation took: {duration_ms:.4f} ms")
    print(f"   Output size: {len(result)}")

if __name__ == "__main__":
    run_benchmark(100_000)
    run_benchmark(10_000_000)
    run_benchmark(50_000_000)