cmake_minimum_required(VERSION 3.12)
project(Developer_Tools VERSION 1.0.0)

option(BUILD_TESTS "Should we build the tests (Requires Python3)?" ON)

if(${BUILD_TESTS})
    enable_testing()
    add_subdirectory(tests)
endif()

