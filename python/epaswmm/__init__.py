"""
EPASWMM Python API

This module provides a Python interface to the EPASWMM library.

"""
import os
import platform
import sys

# Adds directory containing swmm libraries to path
if platform.system() == "Windows":
    lib_dir = os.path.join(sys.prefix, 'bin')
    if hasattr(os, 'add_dll_directory'):
        conda_exists = os.path.exists(os.path.join(sys.prefix, 'conda-meta'))
        if conda_exists:
            os.environ['CONDA_DLL_SEARCH_MODIFICATION_ENABLE'] = "1"
        os.add_dll_directory(lib_dir)
    else:
        os.environ["PATH"] = lib_dir + ";" + os.environ["PATH"]

from .epaswmm import *
from . import solver
from . import output
