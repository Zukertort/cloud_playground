import quant_engine
import numpy as np
import time

def get_weights_ffd(d, thres):
    """
    Calculates the weights for the fractional differentiation.
    d: The fractional order (e.g., 0.4)
    thres: Threshold to cut off weights (e.g., 1e-5)
    """
    w, k = [1.], 1
    while True:
        w_k = -w[-1] / k * (d - k + 1)
        if abs(w_k) < thres:
            break
        w.append(w_k)
        k += 1
    return np.array(w[::-1]).reshape(-1, 1)

def frac_diff_ffd(series, d, thres=1e-3):
    """
    Applies Fractional Differentiation to a pandas Series or numpy array.
    Returns: A numpy array of the differentiated series.
    """
    w = get_weights_ffd(d, thres)
    width = len(w) - 1
    # print(f"DEBUG: FracDiff Window Width: {width} rows")
    
    output = []
    
    data = series.to_list() if hasattr(series, "to_list") else list(series)

    if width >= len(data):
        print(f"WARNING: Dataset ({len(data)} rows) is smaller than FracDiff Window ({width} rows). Returning all NaNs.")
        return np.full(len(data), np.nan)
    
    for i in range(len(data)):
        if i < width:
            output.append(np.nan)
            continue
            
        window = data[i-width : i+1]
        val = np.dot(w.T, window)[0]
        output.append(val)
        
    return np.array(output)

def run_benchmark(size):
    print(f"\n--- Benchmarking FracDiff: {size:,} rows ---")
    
    prices = np.cumsum(np.random.randn(size) + 100).astype(np.float64)
    
    d = 0.4
    thres = 1e-4

    start = time.perf_counter()
    res_cpp = quant_engine.fractional_diff(prices, d, thres)
    end = time.perf_counter()
    print(f"C++ Time: {(end - start) * 1000:.4f} ms")
    
    start = time.perf_counter()
    res_py = frac_diff_ffd(prices, d, thres)
    end = time.perf_counter()
    print(f"Py Time:  {(end - start) * 1000:.4f} ms")

if __name__ == "__main__":
    # Warmup
    run_benchmark(10_000)
    # Test
    run_benchmark(10_000_000)