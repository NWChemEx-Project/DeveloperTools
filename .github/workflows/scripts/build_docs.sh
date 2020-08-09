#!/bin/sh
arch="Linux-x86_64"
cmake_command=cmake-${cmake_version}-${arch}/bin/cmake

# Step 1: Build the Doxygen documentation
${cmake_command} -H. -Bbuild -DBUILD_DOCUMENTATION=ON
${cmake_command} --build build --target cxx_api

# Step 2: Migrate the Doxygen documentation to the docs source
mkdir docs/build
mkdir docs/build/html
mv build/html docs/build/html/cxx_api

#Step 3: Build the Sphinx documentation
source venv/bin/activate
cd docs
make html
