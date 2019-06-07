Writing Tutorials
=================

The purpose of tutorials in the NWX project are to familiarize a developer/user
with a class or concept. Tutorials walk the reader through a simplistic scenario
explaining the logic along the way. This is to be contrasted with the class and
function documentation which usually focuses on what arguments can and cannot be
passed to the class/function.

By their nature tutorials couple source code to documentation. Historically in
electronic structure theory there has been a propensity to write tutorials (if
tutorials were written at all) as part of the documentation. The problem with
this approach is that the tutorial is just text and need not reflect the current
state of the code. Consequentially, it becomes possible for the code's API to
change and for the developer to forget to update the tutorial. The NWX project
solves this problem using the ``scripts/make_tutorial.py`` script.

Tutorial Markdown
-----------------

NWX's documentation is Sphinx-flavored reST. Thus in order for a tutorial to be
included in the documentation it must be converted to reST. To do this we have
written a script, ``scripts/make_tutorial.py``, that will parse a source file's
comments and turn them into a reST file. The tutorial itself should be written
like a typical source file with extended block comments explaining the code.
Block comments meant to be converted verbatim to reST start with the keyword
``TUTORIAL``. These comments form the narrative of the tutorial. Any line of
code not part of a tutorial comment is part of a code block by default. Code
blocks will be added to the resulting ``.rst`` file, verbatim, as
``.. code-block:: x`` directives. To denote a block of code as neither a
tutorial comment or a code block the code can be fenced off with
``TUTORIAL_START_SKIP`` and ``TUTORIAL_STOP_SKIP``.

The ``make_tutorial.py`` script makes a number of assumptions about how you
write your tutorial comments:

1. C/C++ comments must use ``//`` as the comment character
2. Python comments must us ``#`` as the comment character
3. Tutorial comment blocks must be contiguous
4. Tutorial comment blocks should be interspersed within code blocks
5. Tutorial keywords must be the first keywords on a line

Example C++ Tutorial
--------------------

This section shows an example of a markdowned C++ source file suitable for use
as a tutorial with the ``make_tutorial.py`` script.

.. code-block:: c++

    #include <catch2/catch.hpp>
    #include <header/with/factorial.hpp>

    //TUTORIAL_SKIP_START
    TEST_CASE("Factorial Tutorial"){
    //TUTORIAL_SKIP_STOP

    //TUTORIAL
    //
    //This tutorial shows you how to use a hypothetical factorial function.
    //
    //Mathematically the factorial function is defined as:
    //
    //.. math::
    //
    //    n! = \prod_{i=1}^n i
    //
    //Note that :math:`\prod_{i=1}^0 = 1` so that :math:`0! = 1`.
    //
    //To use the factorial function simply provide it the value of ``n``

    auto three_she_bang = factorial(3);
    REQUIRE(three_she_bang == 3*2*1);

    //TUTORIAL_SKIP_START
    } // end test case
    //TUTORIAL_SKIP_STOP

The tutorial should be self-explanatory for the most part. We start by including
the header files for the function. Next we start a Catch2 test case. This allows
us to test the source file easier. The reader of the tutorial doesn't need to
see that though so we fence it off. The tutorial then proceeds with some prose
about what the factorial function is and the syntax of the function's API. As
far as the reader is concerned the last part of the tutorial is the code
example, which follows the tutorial comment; however, the real end of the
tutorial is the fenced off end to the test case. As you can see the above is a
perfectly legitimate C++ source file. Consequentially it can be included as a
unit test to ensure that if the API changes, the tutorial will break.

Assuming the above is stored in a file ``cxx_tutorial.cpp``, parsing the above
unit test should yield the following reST file:

.. code-block:: rest

    CXX Tutorial
    ============

    .. code-block:: c++

        #include <catch2/catch.hpp>
        #include <header/with/factorial.hpp>

    This tutorial shows you how to use a hypothetical factorial function.

    Mathematically the factorial function is defined as:

    .. math::

        n! = \prod_{i=1}^n i

    Note that :math:`\prod_{i=1}^0 = 1` so that :math:`0! = 1`.

    To use the factorial function simply provide it the value of ``n``

    .. code-block:: c++

        auto three_she_bang = factorial(3);
        REQUIRE(three_she_bang == 3*2*1);
