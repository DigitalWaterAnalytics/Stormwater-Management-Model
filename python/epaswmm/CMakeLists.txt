# Description: CMake configuration for epaswmm python library
# Created by: Caleb Buahin (EPA/ORD/CESER/WID)
# Created on: 2024-11-19

# Add Cython targets for epaswmm
add_cython_target(epaswmm epaswmm.pyx CXX PY3)

# Create Python extension modules
add_library(epaswmm MODULE ${epaswmm})

python_extension_module(epaswmm)

# Install the epaswmm module
install(TARGETS epaswmm LIBRARY DESTINATION epaswmm)

# Include the current source directory
target_include_directories(
    epaswmm PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
)

# Add subdirectories
add_subdirectory(output)
add_subdirectory(solver)