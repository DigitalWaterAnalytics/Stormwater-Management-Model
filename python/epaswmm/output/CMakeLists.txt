# CMake configuration for epaswmm python library
#
# Created by: Caleb Buahin (EPA/ORD/CESER/WID)
# Created on: 2024-11-19


add_cython_target(output output.pyx CXX PY3)
add_library(output MODULE ${output})
target_link_libraries(output swmm-output)

python_extension_module(output)
install(TARGETS output LIBRARY DESTINATION epaswmm/output)

target_include_directories(
    output PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    $<TARGET_PROPERTY:swmm-output,INCLUDE_DIRECTORIES>
)
