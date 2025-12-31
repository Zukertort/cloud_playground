#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <cmath>
#include <vector>
#include <algorithm>
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

    {
        py::gil_scoped_release release;

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
    }

    return result;
}

std::vector<double> get_weights_ffd(double d, double thres) {
    std::vector<double> w;
    w.push_back(1.0);
    double k = 1.0;

    while (true) {
        double w_last = w.back();
        double w_k = -w_last / k * (d - k + 1.0);
        if (std::abs(w_k) < thres) break;
        w.push_back(w_k);
        k += 1.0;
    }

    std::reverse(w.begin(), w.end());
    return w;
}

py::array_t<double> fractional_diff(py::array_t<double> input_array, double d, double thres) {
    auto input = input_array.unchecked<1>();
    long long size = input.shape(0);
    
    std::vector<double> weights = get_weights_ffd(d, thres);
    long long width = static_cast<long long>(weights.size());

    auto result = py::array_t<double>(size);
    auto output = result.mutable_unchecked<1>();
    
    if (size < width) {
        for (long long i = 0; i < size; ++i) {
            output(i) = std::nan("");
        }

        return result;
    }

    for (long long i = 0; i < width - 1; ++i) {
        output(i) = std::nan("");
    }

    {
        py::gil_scoped_release release;

        #pragma omp parallel for schedule(static)
        for (long long i = width - 1; i < size; ++i) {
            double dot_product = 0.0;
            
            for (long long j = 0; j < width; ++j) {
                long long price_idx = (i - width + 1) + j;
                dot_product += weights[j] * input(price_idx);
            }
            
            output(i) = dot_product;
        }

    }

    return result;
}

PYBIND11_MODULE(quant_engine, m) {
    m.doc() = "C++23 Quant Engine";
    m.def("calculate_volatility", &calculate_volatility, "Calculate Rolling Volatility");
    m.def("fractional_diff", &fractional_diff, "Calculate FFD");
}