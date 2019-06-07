find_package(Python3 REQUIRED)

add_test(
    NAME make_tutorials
    COMMAND ${Python3_EXECUTABLE}
            ${CMAKE_CURRENT_SOURCE_DIR}/test_make_tutorials.py
)
