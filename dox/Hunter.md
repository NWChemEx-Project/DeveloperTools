Working With Hunter
===================

NWChemEx uses the Hunter C++ package manager throughout.  The official website
for Hunter is [here](https://github.com/ruslo/hunter) and the official 
documentation is [here](https://docs.hunter.sh/).  We've tried to make this
process as painless as possible for new developers.

Using Hunter in a New Repo
--------------------------

This section covers how to add Hunter to a repo.  This will only get your 
project building, it will not add it to the Hunter package manager (we'll cover
that below).  For the purposes of this tutorial we'll assume your entire repo
is included in a directory `my_repo`.  `my_repo` thus is the directory you get
when you check it out of GitHub.

The first step is to add the following boilerplate to `my_repo/CMakeLists.txt`:

```.cmake
cmake_minimum_required(VERSION 3.6)
file(
        DOWNLOAD
        https://github.com/NWChemEx-Project/DeveloperTools/raw/master/cmake.tar.gz
        ${CMAKE_BINARY_DIR}/cmake.tar.gz)
execute_process(
        COMMAND ${CMAKE_COMMAND} -E tar xzf ${CMAKE_BINARY_DIR}/cmake.tar.gz
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)
include(${CMAKE_BINARY_DIR}/cmake/Macros.cmake)
start_hunter(LOCAL) #Must be before project command

project(${project} VERSION 0.0.0 LANGUAGES CXX)

### Options ###
option(BUILD_TESTS "Should we build the tests?" ON)

### Dependencies ####
hunter_add_package(${depend1})
find_package(${depend1} CONFIG)

### Target ###
add_subdirectory(${src_directory})

### Testing ###
if(${BUILD_TESTS})
    enable_testing()
    add_subdirectory(${test_dir})
endif()
```

Feel free to change the minimum CMake version as needed.  The next two commands
respectively retrieve a tarball from the DeveloperTools repo and untar it.  This
tarball contains a couple CMake scripts whose contents won't change often, but
must be included in your project in order for you to be able to use the 
following commands (check out the Convenience Functions section below for 
the full list).  The fourth and fifth lines load our macros and then start
Hunter.  Note the `LOCAL` argument to Hunter indicates that your project 
contains a `cmake/Hunter/config.cmake` file with local Hunter options.  We'll
get to that below in the Fine-Tuning Hunter section; for now note that if your 
project does not have such a file leave the `LOCAL` argument out of the call 
to `start_hunter`.

The remainder of the script is slightly tweaked CMake, whose contents will vary
a bit depending on your project.  `project` is the usual CMake command for 
declaring a project (your project name would replace the placeholder variable
 ${project}).  Next we establish any CMake options that can be used to control
 your project.  Bare minimum this should include the ability to turn off tests,
 as building tests does not make sense for your downstream dependencies.  Other
 possibilities include toggling on optional code, or selecting from among 
 several libraries.  With the options declared we find our dependencies.  Each
 dependency needs to first be run through Hunter using `hunter_add_package`
 before the usual CMake `find_package` command can be invoked.  With all 
 dependencies found we tell CMake to descend into our source directory, and then
 into the testing directory (assuming `BUILD_TESTS` evaluates to `TRUE`).  
 That's the end of the top-level `CMakeLists.txt`.
  
 
 The CMake files within the source and testing directory are pure CMake.  
 Typically this requires a large amount of boilerplate (particularly for 
 installing targets) so we have defined the following CMake functions (they 
 will be in scope thanks to the `include` line):

Fine-Tuning Hunter
------------------

We mentioned above that if your project had local Hunter options it needs to 
contain a `cmake/Hunter/config.cmake` file; for brevity we refer to this file
as the `config.cmake` file for the remainder of this section.  The 
`config.cmake` file can be used to set a variety of per dependency options.  As 
the Hunter manual is a bit difficult to read sometimes, explanations are given 
below for some of the more common uses.

### Non-release dependency

Like most package managers, Hunter relies on a versioning system to keep 
packages straight.  Particularly during development it is common to not have
any formal releases.  This does not play well with Hunter's default 
dependency mechanism.  Instead one includes the following in their 
`config.cmake` file:

```.cmake
hunter_config(
        ${dependency_name}
        VERSION ${version}
        URL "${gh_repo}?access_token=${token}"
        SHA1 "42446742165e643a10778f4a3402a5164728d0bb"
        CMAKE_ARGS "BUILD_TESTS=off"
)
```

where `${dependency_name}` is the name given to `hunter_add_package` and 
`find_package`, `${version}` is some arbitrary tag you're assigning to the
source code (it's best that this is something like `"master"` or `"devel"` so 
that it doesn't clobber real releases).  The next line is the website to pull
the tar of the repo from.  Assuming you are using GitHub, the `${gh_repo}` part
is of the form:

```.cmake
https://api.github.com/repos/${organization}/${repo}/tarball/master
```

where `${organization}` is the name of the organization (or user) hosting the
repo and `${repo}` is the name of the repo.  `master` can be changed to get a
different branch or commit hash.  The remainder of the URL (the "?" forward) is
only necessary if the repo is private.  In that case you'll need to generate a
token that has sufficient rights to access the private repo; the value of that
token should replace `${token}`.

After the URL is the SHA1 hash.  Hunter requires this for security purposes. 
You'll need to generate one yourself.  Easiest way is the `sha1sum` command in
Linux.  Finally, the command takes CMake arguments to pass to the dependency.
In this case we tell it that we don't want it to build the tests.
  
Adding a New Package to Hunter
------------------------------

To be written.

Convenience Functions
---------------------

This section contains the documentation for the convenience functions we have
defined to make your life easier.

### start_hunter

As the name implies this function is used to wrap the call to Hunter.  To use it
you must have a `HunterGate.cmake` file (one comes with the tarball).

Syntax:

```.cmake
start_hunter(
    [LOCAL] # Specify LOCAL to use "cmake/Hunter/config.cmake" file
)
```

Global variables used:
- `CMAKE_BINARY_DIR` : to get the path to the build directory  

### add_nwx_library

Sets up a CMake target that can eventually be passed to `install_targets`.  By
default the target will assume all include paths are relative to the directory
in which the CMake `project` command was run.

Syntax:
```.cmake
add_nwx_library(
    NAME <name> # The name of the resulting target and base name of library
    SOURCES src1 [src2 [...]]] # List of source files to compile
    [DEPENDS depend1 [ depend2 [...]]] # Targets library should be linked to
)    
```

Global variables used:
- `PROJECT_SOURCE_DIR` : To get the root of the CMake project.

### add_python_module

This allows one to declare a C++ target that will be usable as a Python 
module with bindings exported using Pybind11.  Note that this will automatically
add Pybind11 as a dependency to your target, so that you will not need to 
include a `add_hunter_package` for it.  It should be noted that this call will 
do nothing to ensure that all dependencies of your library are compiled with 
position independent code (usually accomplished by passing 
`BUILD_SHARED_LIBS=TRUE` to their CMake build).  

Syntax:
```.cmake
add_python_module(
    NAME <name> # Name of target and library (no prefix/suffix to lib name)
    SOURCES src1 [src2 [...]] # List of source files
    [DEPENDS depend1 [depend2 [...]]] # List of targets library depends on 
)    
```

Global variables used:
- `PROJECT_NAME` : Used for the install RPATH


### add_catch_cxx_tests

This function will add a new Catch2 test given a list of C++ source files to
compile and, optionally, the targets to link against.  This function will
automatically include Catch2 for you so no need to `add_hunter_package` it
yourself.

Syntax:
```.cmake
add_catch_cxx_tests(
  NAME <name> #Name of the resulting test (and executable) 
  SOURCES src1 [ src2 [...]] #A list of source files to use for the test
  [DEPENDS depend1 [depend2 [...]]] #A list of targets to link against
)
```

### add_python_test

This function will create a test that is executed by calling `python3` on the
a script.  The script must have the same name as the test (and the extension 
`.py`).  `PYTHONPATH` will be set to the build directory.  So all includes 
should be relative to it.

Syntax:
```.cmake
add_python_test(
    NAME <name> # The name of the test and script
)
```

Global variables used:
- `CMAKE_BINARY_DIR` : to get the path to the build directory

### install_targets

This is a wrapper around the very large amount of boilerplate required to 
properly install a series of targets from CMake.  We admittedly make several
assumptions about what you want:

1. We assume you want a typical GNU install
   - Headers in `include/<project name>`
   - Libraries in `lib/<project name>`
   - Executables in `bin/`
   - CMake config files in `lib/cmake/<project name>`
2. The configure file will be set up so that the targets can be linked against
   using the syntax `<project name>::<target name>`
3. Your project uses semantic versioning 
   - *i.e.* version X.Y can be used with X.Z for all X, Y, and Z   


Syntax:
```.cmake
install_targets(
    TARGETS target1 [target2 [...]] # Targets to install
    [INCLUDES inc1 [inc2 [...]]] # List of includes to install  
```

Global variables used:
- `PROJECT_NAME` : Used to namespace protect includes, libraries, config files
                   and targets
- `PROJECT_VERSION` : To get project's version information                   
- `CMAKE_CURRENT_BINARY_DIR` : Used to get build directory                 
