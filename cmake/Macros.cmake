#This file contains macros that are useful for taking care of boilerplate in
#CMakeLists.txt.  They may require tweaking to satisfy your particular
#situation.

########## Internal Functions ##################

#Used to make sure a variable is set
function(__assert_arg_set __variable __msg)
    if(NOT DEFINED ${__variable})
        message(AUTHOR_WARNING "${__msg} : ${__variable} not defined")
    endif()
    if("${${__variable}}" STREQUAL "")
        message(AUTHOR_WARNING "${__msg} : ${__variable} is empty")
    endif()
endfunction()

############## Public API Functions #####################

#Must be a macro so Hunter's variables permeate the environment
macro(start_hunter)
    #Change this and the next line to change the version of hunter used
    set(__HUNTER_VERSION "v0.22.14")
    set(__HUNTER_SHA1 "f194eab02248f7d8792f7fc0158f6194d005bf86")

    #Assemble the GitHub URL to use
    set(__GH_URL "https://github.com/ruslo/hunter/archive/")
    set(__GH_URL "${__GH_URL}${__HUNTER_VERSION}.tar.gz")

    cmake_parse_arguments(__START_HUNTER "LOCAL" "" "" ${ARGN})
    #Include and call Hunter
    include("${CMAKE_BINARY_DIR}/cmake/HunterGate.cmake")
    if(${__START_HUNTER_LOCAL})
        HunterGate(URL "${__GH_URL}" SHA1 "${__HUNTER_SHA1}" LOCAL)
    else()
        HunterGate(URL "${__GH_URL}" SHA1 "${__HUNTER_SHA1}")
    endif()
endmacro()

function(add_nwx_library)
    set(__T_KWARGS)
    set(__O_KWARGS NAME)
    set(__M_KWARGS SOURCES DEPENDS)
    cmake_parse_arguments(
            __nwx_lib "${__T_KWARGS}" "${__O_KWARGS}" "${__M_KWARGS}" ${ARGN}
    )
    __assert_arg_set(__nwx_lib_NAME "add_nwx_library")
    __assert_arg_set(__nwx_lib_SOURCES "add_nwx_library")
    if(BUILD_SHARED_LIBS)
        # Set up the RPATH so that the build tree uses the locations of the
        # libraries during the build and during the install the RPATHS are changed
        # to represent their final values
        SET(CMAKE_SKIP_BUILD_RPATH  FALSE)
        SET(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)
        SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_LIBDIR}/${PROJECT_NAME}")
        SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
    endif()

    add_library(${__nwx_lib_NAME} ${__nwx_lib_SOURCES})
    target_include_directories(
            ${__nwx_lib_NAME} PUBLIC
            $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}>
            $<INSTALL_INTERFACE:include>
    )
    target_compile_features(${__nwx_lib_NAME} PUBLIC cxx_std_17)
    if(NOT "${__nwx_lib_DEPENDS}" STREQUAL "")
        target_link_libraries(${__nwx_lib_NAME} ${__nwx_lib_DEPENDS})
    endif()
endfunction()

function(add_python_module)
    hunter_add_package(pybind11)
    find_package(pybind11 CONFIG REQUIRED)
    set(__O_KWARGS NAME)
    set(__M_KWARGS SOURCES DEPENDS)
    cmake_parse_arguments(
            __ADD_PYTHON "" "${__O_KWARGS}" "${__M_KWARGS}" ${ARGN}
    )
    __assert_arg_set(__ADD_PYTHON_NAME "add_python_module")
    __assert_arg_set(__ADD_PYTHON_SOURCES "add_python_module")
    include(GNUInstallDirs)

    # Python needs a shared library (or a module)
    set(BUILD_SHARED_LIBS TRUE)
    add_nwx_library(
            NAME ${__ADD_PYTHON_NAME}
            SOURCES ${__ADD_PYTHON_SOURCES}
            DEPENDS ${__ADD_PYTHON_DEPENDS}
    )
    set_target_properties(
            ${__ADD_PYTHON_NAME} PROPERTIES
            PREFIX ""
            DEBUG_POSTFIX ""
            RELEASE_POSTFIX ""
    )

    #Note do not link against pybind11::module as this will hide the symbols
    #preventing the resulting library from being usable as anything but a Python
    #module
    target_link_libraries(
            ${__ADD_PYTHON_NAME} pybind11::pybind11 pybind11::embed
    )
endfunction()

function(add_catch_cxx_tests)
    set(__O_KWARGS NAME)
    set(__M_KWARGS SOURCES DEPENDS)
    cmake_parse_arguments(
            __CATCH_TEST "" "${__O_KWARGS}" "${__M_KWARGS}" ${ARGN}
    )
    __assert_arg_set(__CATCH_TEST_NAME "In add_catch_cxx_tests")
    __assert_arg_set(__CATCH_TEST_SOURCES "In add_catch_cxx_tests")
    enable_testing()
    hunter_add_package(Catch)
    find_package(Catch2 CONFIG REQUIRED)
    add_executable(${__CATCH_TEST_NAME} "${__CATCH_TEST_SOURCES}")
    target_link_libraries(
            ${__CATCH_TEST_NAME} PRIVATE Catch2::Catch ${__CATCH_TEST_DEPENDS}
    )
    add_test(NAME "${__CATCH_TEST_NAME}" COMMAND ${__CATCH_TEST_NAME})
endfunction()

function(add_python_test)
    set(__O_KWARGS NAME)
    cmake_parse_arguments(__PY_TEST "" "${__O_KWARGS}" "" ${ARGN})
    __assert_arg_set(__PY_TEST_NAME "In add_python_test")
    set(__SCRIPT_NAME ${__PY_TEST_NAME}.py)
    # This is a easy way to copy a file to the build directory keeping the
    # relative path
    configure_file(${__SCRIPT_NAME} ${__SCRIPT_NAME} COPYONLY)

    add_test(NAME ${__PY_TEST_NAME} COMMAND python3 ${__SCRIPT_NAME})
    set_tests_properties(
            ${__PY_TEST_NAME}
            PROPERTIES ENVIRONMENT "PYTHONPATH=${CMAKE_BINARY_DIR}"
    )
endfunction()


# Stolen from Hunter examples.
function(install_targets)
    set(__M_KWARGS TARGETS INCLUDES)
    cmake_parse_arguments(__install "" "" "${__M_KWARGS}" ${ARGN})
    __assert_arg_set(__install_TARGETS "In install_targets")
    message("${__install_TARGETS}")
    # Introduce variables:
    # * CMAKE_INSTALL_LIBDIR
    # * CMAKE_INSTALL_BINDIR
    # * CMAKE_INSTALL_INCLUDEDIR
    include(GNUInstallDirs)

    # Layout. This works for all platforms:
    #   * <prefix>/lib*/cmake/<PROJECT-NAME>
    #   * <prefix>/lib*/
    #   * <prefix>/include/
    set(__config_install_dir "${CMAKE_INSTALL_LIBDIR}/cmake/${PROJECT_NAME}")

    # Directory where the generated files will be stored.
    set(__generated_dir "${CMAKE_CURRENT_BINARY_DIR}/generated")

    # Configuration
    set(
        __version_config "${__generated_dir}/${PROJECT_NAME}ConfigVersion.cmake"
    )
    set(__project_config "${__generated_dir}/${PROJECT_NAME}Config.cmake")
    set(TARGETS_EXPORT_NAME "${PROJECT_NAME}Targets")
    set(__namespace "${PROJECT_NAME}::")

    # Include module with fuction 'write_basic_package_version_file'
    include(CMakePackageConfigHelpers)

    # Configure '<PROJECT-NAME>ConfigVersion.cmake'
    # Use:
    #   * PROJECT_VERSION
    write_basic_package_version_file(
            "${__version_config}" COMPATIBILITY SameMajorVersion
    )

    # Configure '<PROJECT-NAME>Config.cmake'
    # Use variables:
    #   * TARGETS_EXPORT_NAME
    #   * PROJECT_NAME
    configure_package_config_file(
            "${CMAKE_BINARY_DIR}/cmake/Config.cmake.in"
            "${__project_config}"
            INSTALL_DESTINATION "${__config_install_dir}"
    )

    # Install targets
    install(
            TARGETS ${__install_TARGETS}
            EXPORT "${TARGETS_EXPORT_NAME}"
            LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}/${PROJECT_NAME}"
            ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}/${PROJECT_NAME}"
            RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
            INCLUDES DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
    )

    #Install headers
    #
    #This next part can be a bit tricky.  We assume that ${__headers} is a list
    #of header files relative to the directory this function was called from.
    #The tricky part is that relative path may contain subdirectories.  If we
    #just tell CMake to install the headers it won't make the subdirectories.
    #To avoid this, we loop over the files, grabbing the directories (if they
    #exist) and append them to the path.
    set(__inc_dir "${CMAKE_INSTALL_INCLUDEDIR}/${PROJECT_NAME}")
    foreach(__header ${__install_INCLUDES})
        get_filename_component(__dir ${__header} DIRECTORY)
        install(FILES ${__header} DESTINATION "${__inc_dir}/${__dir}")
    endforeach()

    # Signal the need to install the config files we just made
    install(
            FILES "${__project_config}" "${__version_config}"
            DESTINATION "${__config_install_dir}"
    )
    install(
            EXPORT "${TARGETS_EXPORT_NAME}"
            NAMESPACE "${__namespace}"
            DESTINATION "${__config_install_dir}"
    )
endfunction()
