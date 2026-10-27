cmake_minimum_required(VERSION 3.22)
project(mesa_cs2_bridge LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(MSVC)
    add_compile_options(/W3 /O2 /EHa /utf-8)
endif()

add_library(mesa_bridge SHARED
    dllmain.cpp
    offsets.hpp
)
target_link_libraries(mesa_bridge PRIVATE Psapi)

add_executable(mesa_injector
    injector.cpp
)

set_target_properties(mesa_bridge mesa_injector PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_CURRENT_SOURCE_DIR}"
    LIBRARY_OUTPUT_DIRECTORY_RELEASE "${CMAKE_CURRENT_SOURCE_DIR}"
)
