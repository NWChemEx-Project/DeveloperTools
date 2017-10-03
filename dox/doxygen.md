Using Doxygen in the NWChemEx Project
=====================================

Documentation Pages
-------------------

Doxygen supports the inclusion of pages (like this one) in your documentation
for discussing involved topics.

TODO: Decide on whether we just want to use markdown, like this page.

TODO: Decide on whether or not Doxygen commands are allowed in the markdown.
*E.g.* `\f$\mu + \nu\f$` would display the Latex command, but GitHub won't
parse it.

TODO: Related to above, decide to what extent we want to have the markdown
pages accessible from GitHub.

Documenting Code
----------------

Doxygen allows you document your code in a minimally invasive manner.  It does
this by slightly modifying the comment characters.  Examples:

~~~.cpp
/// This is a Doxygen, single-line comment for the following function  
void function1();  
 
//! This is an alternative syntax for a single-line comment  
void function2();
  
/** For more extened documentation block comments are preferred.
    This line is also part of the comment.
 */
void function3();
  
/*! The exclamation syntax also works for block comments.
    Still in block comment
 */
~~~

TODO: Decide on either the `///` and `/** */` or the `//!` and `/*! */` syntax

Documentation in Doxygen comes in two types: brief and detailed.  Brief
documentation, as the name implies, is meant to quickly convey what a function
does.  Parts of the documentation will contain lists of functions/members and it
will be the brief documentation that is displayed.  Detailed documentation is
meant for telling all of the details of a function.

Minimal Documentation Standards
-------------------------------

To aid in documenting Doxygen provides a host of keywords (triggered by either
a "\" or "@" character *e.g.* `\param` or `@param`).  By far the most useful
ones are shown in the following code example, which should be taken as a
minimal acceptable standard.

~~~.cpp

/** \brief This is the brief description of fake function 1.
 
    Fake function 1 demonstrates the bare minimal documentation standards. This
    is the detailed description that will show up in the documentation.
    
    \param[in] Param1 The first parameter; it's read-only.
     
    \param[out] Param2 The second parameter; it's going to be written to.
     
    \param[in,out] Param3 The third parameter; it's going to be read from and
        written to. 
                          
    \returns Whatever this function returns.
    
    \tparam T The type this function takes.  It should satisfy XXX concept.
    
    \throws std::runtime_error Throws if some condition is tripped.  Weak 
                               exception guarantee.
 */
 template<typename T>
 int function1(int Param1, int& Param2, int& Param3);
 ~~~
 
 Obviously the real documentation should be more helpful, but this illustrates
 the key descriptions: the brief, the detailed description, the input/output 
 parameters, the return value, any template type (or non-type) parameters, and
 any exceptions that are thrown (as well as the level of exception guarantee).
 
 TODO: Decide whether we want to use the `\` or `@` syntax.
 
 TODO: Any other minimal requirements?  Thread safety?