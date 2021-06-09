*********************************
Development Workflow for NWChemEx
*********************************

Compared to other electronic structure packages, NWChemEx has a fairly different
source structure. This page will walk you through how to get up and developing
with NWChemEx. Right now we only include directions for developing in C++,
directions will be updated with Python instructions as they become available.

.. _Workflow Preliminaries:

Preliminaries
=============

This page assumes that you are familiar with the property type/module
abstractions and have a general idea of what goes into each repository. If this
is not the case see here (TODO: Add a useful link).

Directory Structure
-------------------

It is strongly recommended you create a folder named something like
``nwx_workspace``. We'll term this directory your NWChemEx workspace. As a bare
minimum you'll want to clone the ``NWChemEx-Project/NWChemEx`` repo into your
workspace (for more help see: :ref:`Git and GitHub Procedures`). More than
likely you will need to clone at least one additional repository, the repo where
your module/code will live. For sake of argument we'll assume that you are
writing a module for use with the SCF. In this case you will also need to clone
the ``NWChemEx-Project/SCF``. Your NWChemEx workspace thus looks like:

.. code-block::

   nwx_workspace/
   |
   |-- NWChemEx/
   |
   |-- SCF/
   |
   `--toolchain.cmake

where the ``toolchain.cmake`` file will be described below.

Basic C++ setup
===============

These instructions really only apply if you are working in a repository that is
directly linked into NWChemEx-Project/NWChemEx. If you are writing C++ modules
as plugins, i.e., outside the core stack, you should follow the instructions
here (TODO: add link).

It is strongly recommended that you make a toolchain file with all of your
compilation options. It's conventional to call this file ``toolchain.cmake`` and
we'll put it just inside the NWChemEx workspace.

TODO: Basic syntax of toolchain file/link to more complicated directions

End users of NWChemEx simply need to build the ``NWChemEx-Project/NWChemEx``
repository. By default the build process will use clean versions of all the
dependencies (*e.g.*, repos like ``NWChemEx-Project/SCF``). For development
purposes we don't want clean versions,the build to use our local
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

With the toolchain file properly configured, when we build
``NWChemEx-Project/NWChemEX`` the build process will use our local version of
each repo we provided a ``FETCHCONTENT_SOURCE_DIR_XXX`` value for. Changes to
say the SCF repo will then be reflected in the NWChemEx repo.
