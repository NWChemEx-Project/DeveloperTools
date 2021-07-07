******************************************
Conventions for Writing reST Documentation
******************************************

Style
=====

The style of reST pages follows Python's
`conventions <https://devguide.python.org/documenting/#documenting-python>`_.
In particular:

- Follow the usual practice of at most 80 characters per line
- Indentation in reST is 3 spaces **NOT** 4

  - 3 spaces is natural for reST as this aligns with directives

Sections
========

NWChemEx adopts Python's reST
`conventions <https://devguide.python.org/documenting/#sections>`_ for denoting
sections. Namely:

- ``#`` with overline should be used for parts
- ``*`` with overline is for chapters
- ``=`` for sections
- ``-`` for subsections
- ``^`` for subsubsections
- ``"`` for paragraphs

The distinction between "parts", "chapters", *etc*. is based largely on how
nested in the documentation a file is. For example, "parts" are topics in the
top-level table of contents; in the case of DeveloperTools' documentation the
parts are: Project Conventions, Design Documentation, *etc.*. Chapters are
topics within one of the parts (*e.g.* this page is a chapter in the Project
Conventions part).
