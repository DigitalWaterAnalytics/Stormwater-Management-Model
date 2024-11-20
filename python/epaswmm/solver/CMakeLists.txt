# CMake configuration for epaswmm library
#
# Created by: Caleb Buahin (EPA/ORD/CESER/WID)
# Created on: 2024-11-19
#

add_cython_target(solver solver.pyx CXX PY3)
add_library(solver MODULE ${solver})
target_link_libraries(solver swmm5)

python_extension_module(solver)
install(TARGETS solver LIBRARY DESTINATION epaswmm/solver)

target_include_directories(
    solver PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    $<TARGET_PROPERTY:swmm5,INCLUDE_DIRECTORIES>
)
