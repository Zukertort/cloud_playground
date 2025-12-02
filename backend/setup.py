from setuptools import setup, Extension
import pybind11

# -std=c++23 : Enable C++23 features
# -O3        : Maximum Optimization (Speed)
# -march=native : Optimize for the specific CPU (AVX2/AVX512 instructions)
cpp_args = ['-std=c++23', '-O3', '-march=native'] 

ext_modules = [
    Extension(
        'quant_engine',
        ['cpp_engine/engine.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=cpp_args,
    ),
]

setup(
    name='quant_engine',
    version='0.1',
    author='Ricardo Gobbi',
    description='A C++ extension for quantitative analysis',
    ext_modules=ext_modules,
)