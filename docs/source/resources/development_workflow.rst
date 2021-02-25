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
``nwx_workspace``. Bare minimum you'll want to clone the 
``NWChemEx-Project/NWChemEx`` repo into your workspace. If you are developing a
module that will live in say the ``NWChemEx-Project/SCF`` repo you will also 
want to clone that repo. For the sake of this page we'll assume you are 
developing a new SCF guess and thus your workspace will look like:

```
nwx_workspace/
|
|---NWChemEx/
|
L---SCF/
```

TODO: Better file structure ASCII art.

Basic C++ setup
===============



Using CLion
===========

While it is possible to use CLion, experience suggests that CLion has trouble
with large C++ projects. Someone who uses CLion should fill in this section.

Using VSCode
============

TODO: Document how to setup VSCode for use with NWX

