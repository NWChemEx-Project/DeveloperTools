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
following commands.  The fourth and fifth lines load our macros and then start
Hunter.  Note the `LOCAL` argument to Hunter indicates that your project 
contains a `cmake/Hunter/config.cmake` file with local Hunter options.  We'll
get to that below; for now note that if your project does not have such a file
leave the `LOCAL` argument out of the call to `start_hunter`.


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
 
 - `add_nwx_library(${my_target} "${SRCS}" "${INCLUDES}")`
   - This function will create a CMake target called `${my_target}` whose source
     files are given by the list `"${SRCS}"` and has public header files given
     by `"${INCLUDES}"`.
   - The result of this call is a legitimate CMake target that will be properly
     installed.  You are free to continue setting it up by including things 
     like the targets it must link against (make sure to include your 
     dependencies!!!)
 - `add_catch_cxx_tests(${test_target} "${test_srcs}" ${target2test})`
   - This function will create a CTest unit test called `${test_target}` that
     uses the Catch testing framework.  The resulting executable will be built
     from the sources in the list `"${test_srcs}"` and will test the target
     library whose CMake target is `${"target2test}`  
   - This function will automatically add Catch as a dependency of your project.
   - This assumes the following is present in only one test's source file.
      ```.cpp
      #define CATCH_CONFIG_MAIN
      #include <catch.hpp>
      ```
### The `cmake/Hunter/config.cmake` File

We mentioned above that if your project had local Hunter options it needs to 
contain a `cmake/Hunter/config.cmake` file; for brevity we refer to this file
as the `config.cmake` file for the remainder of this section.  The 
`config.cmake` file can be used to set a variety of per dependency options.  As 
the Hunter manual is a bit difficult to read sometimes, explanations are given 
below for some of the more common uses.

#### Non-release dependency

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
