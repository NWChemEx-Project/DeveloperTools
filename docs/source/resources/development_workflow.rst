*********************************
Development Workflow for NWChemEx
*********************************

Compared to other electronic structure packages, NWChemEx has a fairly different
source structure. This page will walk you through how to get up and developing
with NWChemEx. Right now we only include directions for developing in C++, 
directions will be updated with Python instructions as they become available.

Preliminaries
=============

This page assumes that you are familiar with the property type/module 
abstractions and have a general idea of what goes into each repository. If this
is not the case see here (TODO: Add a useful link).

It is strongly recommended you create a folder named something like 
``nwx_workspace``. We'll term this directory your NWChemEx workspace. As a bare 
minimum you'll want to clone the ``NWChemEx-Project/NWChemEx`` repo into your 
workspace (TODO: Add a link to the git tutorial). More than likely you will need
to clone at least one additional repository, the repo where your module/code 
will live. For sake of argument we'll assume that you are writing a module for
use with the SCF. In this case you will also need to clone the 
``NWChemEx-Project/SCF``. Your NWChemEx workspace thus looks like:

.. code-block::

   nwx_workspace/
   |
   |---NWChemEx/
   |
   L---SCF/

TODO: Better file structure ASCII art.

Basic C++ setup
===============

It is strongly recommended that you make a toolchain file with all of your
compilation options. It's conventional to call this file ``toolchain.cmake`` and
we'll put it just inside the NWChemEx workspace.

TODO: Basic syntax of toolchain file/link to more complicated directions

End users of NWChemEx simply need to build the ``NWChemEx-Project/NWChemEx`` 
repository. By default the build process will use clean versions of all the 
dependencies (*e.g.*, repos like ``NWChemEx-Project/SCF``). For development 
purposes we don't want clean versions, rather we want the build to use our local 
versions. To make sure the NWChemEx-Project uses our local version of the SCF 
repo we set the CMake variable ``FETCHCONENT_SOURCE_DIR_SCF`` to the 
``NWChemEx-Project/SCF`` repository in our NWChemEx workspace. This is done by
adding a line like:

.. code-block:: cmake

   set(FETCHCONENT_SOURCE_DIR_SCF /full/path/to/nwx_workspace/SCF)

to our toolchain file. Additional local versions of repositories can be added 
using the analogous ``FETCHCONENT_SOURCE_DIR_XXX`` variables (``XXX`` is the 
uppercase name of the repo as defined in the build files).

TODO: Table of valid XXX values and the corresponding repo

With the toolchain file properly configured we build ``NWChemEx-Project/SCF``.
In the ``nwx_workspace/NWChemEx`` directory we execute

IDEs
====

While you can develop code for NWChemEx purely from the terminal you'll probably
be more productive if you use an integrated development environment (IDE). IDEs
are intimidating at first, but once you get them setup, and log some hours, 
you'll never go back to command line development again. Advantages of using an
IDE include (this is a union of features from across IDEs; most IDEs support 
most of the features on this list, but they may not support all of them):

- Built-in debugging
 
  - Click to add break points
  - Easily inspect variable values

- Code inspection

  - Shows you errors/warnings without you having to compile
  - Can suggest best practices 

- Code autocomplete

  - Auto inserts closing braces, brackets, etc.
  - Knows about classes, variables, etc. so you only need to type the first few
    letters

- Automatic formatting

  - No more forgetting to run ``clang-format``!!!!
   
- Typically a single click to build/debug
- Built in version control
- Syntax highlighting

  - Makes reading code much easier

- Code folding
  
  - Allows you to hide irrelevant parts of the code


This section walks you through setting up NWChemEx development environments with
several popular IDEs.

CLion
-----

While it is possible to use CLion, experience suggests that CLion has trouble
with large C++ projects. Someone who uses CLion should fill in this section.

VSCode
------

Visual Studio Code, or VSCode, is an IDE from Microsoft. Despite being from 
Microsoft, VSCode is free, has a Linux version, and is suprisingly light weight 
for C++ development.

By default VSCode is pretty bare bones. Additional features are added/enabled by
installing extensions. When you load up source code VSCode will inspect it and
automatically recommend you install the corresponding extenstion (if it's not
installed already).

TODO: Document how to setup VSCode for use with NWX

FAQs
^^^^

This subsection covers frequently asked questions regarding VSCode.

**How do I get the reST extension to use a virtual environment?**

Assuming you have created a virtual environment ``venv`` and installed all of
your reST/Sphinx dependencies in to it. Start by using ctrl+shift+p to bring up 
the command palette. Then select ``Python: Select Interpreter``. Navigate to
``venv/bin/python3``. Now the reST extension should use the virtual environment
``venv`` for rendering your documentation preview.
`Source <https://stackoverflow.com/questions/58433333/auto-activate-virtual-environment-in-visual-studio-code>`_.



