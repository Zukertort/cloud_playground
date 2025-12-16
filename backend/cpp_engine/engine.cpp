#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cmath>
#include <omp.h>

namespace py = pybind11;

py::array_t<double> calculate_volatility(py::array_t<double> input_array, int window) {
    auto input = input_array.unchecked<1>();
    
    long long size = input.shape(0);
    long long win = static_cast<long long>(window);

    if (size < win) return py::array_t<double>();

    auto result = py::array_t<double>(size);
    auto output = result.mutable_unchecked<1>();

    for(long long k = 0; k < win - 1; k++) {
        output(k) = 0.0;
    }

    #pragma omp parallel for schedule(static)
    for (long long i = win - 1; i < size; ++i) {
        
        double sum = 0.0;
        for (long long j = i - win + 1; j <= i; ++j) {
            sum += input(j);
        }
        double mean = sum / win;

        double sq_sum = 0.0;
        for (long long j = i - win + 1; j <= i; ++j) {
            double diff = input(j) - mean;
            sq_sum += diff * diff;
        }
        
        output(i) = std::sqrt(sq_sum / win);
    }

    return result;
}

PYBIND11_MODULE(quant_engine, m) {
    m.doc() = "Safe Parallel C++ Quant Engine";
    m.def("calculate_volatility", &calculate_volatility, "Calculate Rolling Volatility");
}