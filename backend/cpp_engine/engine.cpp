#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <cmath>
#include <numeric>

namespace py = pybind11;

// A simple function to calculate Rolling Volatility (Standard Deviation)
// This mimics what we did in Polars, but on raw vectors for low-latency.
std::vector<double> calculate_volatility(const std::vector<double>& prices, int window) {
    std::vector<double> volatility;
    
    if (prices.size() < window) {
        return volatility; // Return empty if not enough data
    }

    for (size_t i = 0; i < prices.size(); ++i) {
        if (i < window - 1) {
            volatility.push_back(0.0); // Padding for the start
            continue;
        }

        // Calculate Mean of window
        double sum = 0.0;
        for (size_t j = i - window + 1; j <= i; ++j) {
            sum += prices[j];
        }
        double mean = sum / window;

        // Calculate Variance
        double sq_sum = 0.0;
        for (size_t j = i - window + 1; j <= i; ++j) {
            sq_sum += std::pow(prices[j] - mean, 2);
        }
        
        // Std Dev
        volatility.push_back(std::sqrt(sq_sum / window));
    }

    return volatility;
}

// The Binding Code (This makes it visible to Python)
PYBIND11_MODULE(quant_engine, m) {
    m.doc() = "C++ Accelerated Quant Engine"; // Optional module docstring
    m.def("calculate_volatility", &calculate_volatility, "Calculate Rolling Volatility");
}