******
VSCode
******

Visual Studio Code, or VSCode, is an IDE from Microsoft. Despite being from
Microsoft, VSCode is free, has a Linux version, and is suprisingly light weight
for C++ development.

Creating a Workspace
====================

When you first start up VSCode you will want to go to
``files->add folder to workspace`` and provide VSCode with one of the NWChemEx
repos in your NWX workspace, *e.g.*, `nwx_workspace/SCF` in the directory
structure assumed in :ref:`Workflow Preliminaries`). Once you have done this you
should see your folder and its subdirectories in the explorer view
(explorer view is the icon with a page overlying a square in the left toolbar).
You can repeat this process for each of the additional NWX repos in your
workspace. It is recommend that you then save your workspace
(File->Save Workspace As) that way you can quickly open all of these repos
again.

.. note::

   AFAIK adding each repo individually in this manner is the only way for the
   CMake extension to properly register the root CMakeLists.txt for each repo.
   If you try to add the workspace root it will instead look for the root
   CMakeLists.txt there.

Adding Extensions
================

By default VSCode is pretty bare bones. Additional features
are added/enabled by installing extensions. When you load up source code VSCode
will inspect it and automatically recommend you install the corresponding
extenstion (if it's not installed already). For developing NWX we recommend you
minimally install:

#. ``ms-vscode.cpptools``
#. ``ms-vscode.cmake-tools``
#. ``ms-python.python``
#. ``lextudio.restructuredtext``

To install an extension click on the extensions view (the icon in the left
toolbar with a square broken into four smaller squares) and search for the
identifiers given in the above list.

Building
========

Once you've minimally added the C++ and CMake extensions it's time to start
setting up your build process. For the purposes of this tutorial we assume you
are using a toolchain file with all of your CMake options. For sake of arguement
we assume that the full path to your toolchain file is given by:
``/home/user/nwx_workspace/toolchain.cmake``.

To modify VSCode's CMake settings click on the gear in the left toolbar and then
settings. You will then be presented with all of VSCode's settings. At the top
you will see three tabs ("User", "Workspace", and the name of your current
folder); these tabs indicate the scope of the settings you are setting (user
settings follow you, workspace settings are for the entire workspace, and folder
setings are only for the current folder). Since building is somewhat project-
specific we recommend you click on either "Workspace" or folder. The CMake
settings are then accessed by expanding the "Extensions" settings and navigating
to "CMake configuration".

Configuring the Build
---------------------

The first step is to set the paths of the CMake executables. If the ``cmake``
and ``ctest`` executables are in your path feel free to skip this step.
Otherwise set "CMake Path" to the full path to your CMake executable. VSCode
will automatically use the ``ctest`` executable that comes with the ``cmake``
executable you specify (but if you want to use a different one you can change
its path below via the "Ctest Path" option).

Next we need to make sure the build uses our toolchain file. For our purposes the main option we need to change is "Configure Args" (do not
confuse this with "Build Tool Args", which are the arguments that get passed to
the underlying build tool, typically ``make``). Under "Configure Args" click on
"Add Item" and type:

.. code-block:: cmake

   -DCMAKE_TOOLCHAIN_FILE=/home/user/nwx_workspace/toolchain.cmake

substituting in your toolchain's path.

Configuring the Project (i.e., running CMake)
---------------------------------------------

Once you've setup the options it's time to actually configure the project. To
configure say SCF, click on a C++ file or a CMake file in the ``SCF`` directory.
The bottom toolbar should show a folder icon with ``SCF`` next to it; this is
how you can tell which project will be configured. In the bottom toolbar you
should also see a panel with something like "CMake: [Debug]: Ready". Click on
this. You will get a pop-up asking you to select a kit. Choose "Unspecified" to
let CMake detect the kit for you (it'll end-up using your toolchain file). Then
pick the build type you want (Debug for normal development). After this you
should see the normal CMake configuration dialog fly by in the terminal. You'll
know it's configured successfully if you get a line like

.. code-block:: bash

   -- Build files have been written to: <your/build/directory/path>

Building the Project
--------------------

Once the project has been configured you simply click the word "Build" in the
toolbar at the bottom. Akin to the configure step, you should see the usual
build dialog fly by on the terminal.

Testing the Project
-------------------

After a successful build you should be able to click the play arrow
(right-facing triangle) to run the resulting executable (assuming you enabled
testing by putting ``BUILD_TESTING=TRUE`` in your toolchain file). Again the
normal testing output will fly by in the terminal.

Developing
==========

Once you've got the build working you're ready to start developing.

Version Control
---------------

It's strongly recommended that you do your development on a new branch and not
on "master" (the bottom toolbar should show your current branch next to the
version control icon, three circles in a V-like pattern). Clicking on the branch
name will bring up a menu where you can select "Create new branch" to create
your new branch (clicking "Create new branch" will lead to a new menu where you
name the branch).

More version control options are available in the left toolbar by clicking on
the version control symbol.

Debugging
---------

Debugging is one of the main reasons to use an IDE. To debug an executable,
click on the play-arrow with a bug on it in the left toolbar. If you have no
debug configurations set up yet there will be a big "Run and Debug" button
Click on it. This will bring up a menu asking you about the type of C++ debugger
you want to use. Pick the appropriate one (probably GDB/LLVM). Next, it'll ask
you which configuration you want to use. This will generate a JSON with your
debug configuration and open it in an editor. For most purposes the only thing
we need to change is the "program" key-value; change this to path to the
executable you want to debug (note you can use ``${workspaceFolder}`` to get an
absolute path to the top-level directory of your current folder; somewhat confusingly .
this is not the path where your workspace is saved).
FAQs
====

This subsection covers frequently asked questions regarding VSCode.

**How do I change the editor font size?**

In settings search "editor.fontSize". Change the field to your preferred font
size.

**How do I get a ruler to signify the 80 character limit?**

In settings search "editor.rulers". Click on the "edit in settings.json" link.
In the ``settings.json file`` add "80" to the settings file that gets opened.

**How do I get the reST extension to use a virtual environment?**

Assuming you have created a virtual environment ``venv`` and installed all of
your reST/Sphinx dependencies in to it. Start by using ctrl+shift+p to bring up
the command palette. Then select ``Python: Select Interpreter``. Navigate to
``venv/bin/python3``. Now the reST extension should use the virtual environment
``venv`` for rendering your documentation preview.
`Source <https://stackoverflow.com/questions/58433333/auto-activate-virtual-environment-in-visual-studio-code>`_.
