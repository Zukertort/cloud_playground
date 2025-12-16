from setuptools import setup, Extension
import pybind11
import sys

cpp_args = ['-std=c++23', '-O3', '-march=native', '-fopenmp']
link_args = ['-fopenmp']

if sys.platform == 'darwin':
    cpp_args = ['-std=c++23', '-O3', '-Xpreprocessor', '-fopenmp']
    link_args = ['-lomp']

ext_modules = [
    Extension(
        'quant_engine',
        ['cpp_engine/engine.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=cpp_args,
        extra_link_args=link_args,
    ),
]

setup(
    name='quant_engine',
    version='0.2',
    author='Ricardo Gobbi',
    description='Parallel C++ extension for quantitative analysis',
    ext_modules=ext_modules,
)