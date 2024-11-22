# CMake configuration for epaswmm library
#
# Created by: Caleb Buahin (EPA/ORD/CESER/WID)
# Created on: 2024-11-19
#

# Find Python
find_package(Python3 REQUIRED COMPONENTS Development)

# Find Python extensions
find_package(PythonExtensions REQUIRED)

# Add Cython target
add_cython_target(solver solver.pyx CXX PY3)

# Add library
add_library(solver MODULE ${solver})

# Link to SWMM and Python libraries
target_link_libraries(solver swmm5 Python3::Python)

# Specify that this is a Python extension module
python_extension_module(solver)

# Install the target
install(TARGETS solver LIBRARY DESTINATION epaswmm/solver)

# Include directories
target_include_directories(
    solver PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    $<TARGET_PROPERTY:swmm5,INCLUDE_DIRECTORIES>
    ${Python3_INCLUDE_DIRS}
)