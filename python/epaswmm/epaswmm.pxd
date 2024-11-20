# Description: Cython module for encoding and decoding SWMM datetimes
# Created by: Caleb Buahin (EPA/ORD/CESER/WID)
# Created on: 2024-11-19

# cython: language_level=3
# python imports
from cpython.datetime cimport datetime

# third-party imports

# project imports

# Define the number of days since 01/01/00
cpdef double encode_swmm_datetime(datetime pdatetime)

# Define the number of days since 01/01/00
cpdef datetime decode_swmm_datetime(double swmm_datetime)