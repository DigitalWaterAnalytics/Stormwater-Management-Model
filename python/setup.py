# Description: This file is used to build the python package for the epaswmm package.
# Created by: Caleb Buahin (EPA/ORD/CESER/WID)
# Created on: 2024-11-19

# python imports
import os
import sys
import platform
import subprocess
from setuptools import Command
from setuptools.command.build_ext import build_ext
import shutil

# third party imports
from skbuild import setup

# local imports


platform_system = platform.system()


def get_version():
    """
    Get version from toolkit
    TODO: This should be revised to get version information from the toolkit
    """
    return "5.3.0.dev0"


if os.environ.get('EPASWMM_CMAKE_ARGS') is not None:
    cmake_args = os.environ.get('EPASWMM_CMAKE_ARGS').split()

elif platform_system == "Windows":
    cmake_args = ["-GVisual Studio 17 2022", "-Ax64"]

elif platform_system == "Darwin":
    cmake_args = [
        "-GNinja", "-DCMAKE_OSX_DEPLOYMENT_TARGET:STRING=10.9",
        "-DCMAKE_OSX_ARCHITECTURES=arm64;x86_64"
    ]

else:
    cmake_args = ["-GUnix Makefiles"]

setup(
    version=get_version(),
    packages=[
        "epaswmm",
    ],
    cmake_args=[
        *cmake_args,
    ],
    include_package_data=True,
    python_requires=">=3.8",
)
