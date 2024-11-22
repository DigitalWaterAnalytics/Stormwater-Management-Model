# CMake configuration for epaswmm python library
#
# Created by: Caleb Buahin (EPA/ORD/CESER/WID)
# Created on: 2024-11-19

# Find Python
find_package(Python3 REQUIRED COMPONENTS Development)
find_package(PythonExtensions REQUIRED)

add_cython_target(output output.pyx LANGUAGE CXX PY3)

# Add Cython target
add_library(output MODULE ${output})

# Add library
target_link_libraries(output swmm-output)

# Specify that this is a Python extension module
python_extension_module(output)

# Install the target
install(TARGETS output LIBRARY DESTINATION epaswmm/output)

# Include directories
target_include_directories(
    output PRIVATE 
    ${CMAKE_CURRENT_SOURCE_DIR}
    $<TARGET_PROPERTY:swmm-output,INCLUDE_DIRECTORIES>
)
