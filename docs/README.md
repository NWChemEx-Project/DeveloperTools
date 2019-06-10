Source Files for Developer Documentation
========================================

This directory contains the source files for NWChemEx's developer documentation.

Building the Documentation
--------------------------

The developer documentation uses Sphinx. If you do not have Sphinx installed
installing it is usually done with Python's `pip` command:

~~~.sh
pip install sphinx sphinx_rtd_theme
~~~

With Sphinx installed the documentation is built by:

~~~.sh
#Run in the same directory as this README
make html
~~~

This will result in HTML documentation, the main index of which will be
located at `<directory_containing_this_readme>/build/html/index.html` and can be
viewed by directing your web browser of choice to that file (this is done by
using `file:///path/to/index.html` as the URL).
