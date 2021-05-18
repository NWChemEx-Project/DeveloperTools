******
VSCode
******

Visual Studio Code, or VSCode, is an IDE from Microsoft. Despite being from
Microsoft, VSCode is free, has a Linux version, and is suprisingly light weight
for C++ development.


Creating a Workspace
====================

When you first start up VSCode you will want to go to
``file->add folder to workspace`` and tell VSCode to add the folder which
contains your NWX workspace (called ``nwx_workspace`` in the assumed directory
structure). Once you have done this you should see your NWX workspace folder and
its subdirectories in the explorer view (explorer view is the one with the page
overlying a square).

Adding Extensions
=================

By default VSCode is pretty bare bones. Additional features
are added/enabled by installing extensions. When you load up source code VSCode
will inspect it and automatically recommend you install the corresponding
extenstion (if it's not installed already). For developing NWX we recommend you
minimally install:

#. ``ms-vscode.cpptools``
#. ``ms-vscode.cmake-tools``
#. ``ms-python.python``
#. ``lextudio.restructuredtext``

To install an extension click on the extensions view (the one with a square
broken into four smaller squares) and search for the identifiers given in the
above list.



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
