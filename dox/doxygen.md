Using Doxygen in the NWChemEx Project
=====================================

Documentation Pages
-------------------

Doxygen supports the inclusion of pages (like this one) in your documentation
for discussing involved topics.

TODO: Decide on whether we just want to use markdown, like this page.

TODO: Decide on whether or not Doxygen commands are allowed in the markdown, 
but realize that GitHub won't parse them.

TODO: Related to above, decide to what extent we want to have the markdown
pages accessible from GitHub.

Documenting Code
----------------

Doxygen allows you document your code in a minimally invasive manner.  It does
this by slightly modifying the comment characters.  Examples (if you are 
viewing this on GitHub ignore the verbatim commands; they're to prevent
Doxygen from parsing the comments):

```
@verbatim
/// This is a Doxygen, single-line comment for the following function  
void function1();  
 
/** For more extened documentation block comments are preferred.
    This line is also part of the comment.
 */
void function3();
@endverbatim
```
Doxygen supports other conventions; however, the two above are the approved
conventions for the NWChemEx project.

Documentation in Doxygen comes in two types: brief and detailed.  Brief
documentation, as the name implies, is meant to quickly convey what a function
does.  Parts of the documentation will contain lists of functions/members and it
will be the brief documentation that is displayed.  Detailed documentation is
meant for telling all of the details of a function.

Minimal Documentation Standards
-------------------------------

To aid in documenting Doxygen provides a host of keywords (triggered by either
a "@" character *e.g.* `@param`; for consistency please do not use the alternative syntax of that uses a "\" character).  By far the most useful
ones are shown in the following code example, which should be taken as a
minimal acceptable standard.

```
@verbatim
/** @brief This is the brief description of fake function 1.
 
    Fake function 1 demonstrates the bare minimal documentation standards. This
    is the detailed description that will show up in the documentation.
    
    @param[in] Param1 The first parameter; it's read-only.
     
    @param[out] Param2 The second parameter; it's going to be written to.
     
    @param[in,out] Param3 The third parameter; it's going to be read from and
        written to. 
                          
    @returns Whatever this function returns.
    
    @tparam T The type this function takes.  It should satisfy XXX concept.
    
    @throws std::runtime_error Throws if some condition is tripped.  Weak 
                               exception guarantee.
 */
 template<typename T>
 int function1(int Param1, int& Param2, int& Param3);
 @endverbatim
 ```
 
 Obviously the real documentation should be more helpful, but this illustrates
 the key descriptions: brief, detailed description, input/output parameters, 
 return value, template type (or non-type) parameters, and exceptions that are
 thrown (as well as the level of exception guarantee).
 
 Other minimal commands motivated by email thread:
- @file for documenting files
- @defgroup used to define groups for organizational reasons
- @ingroup for associating a file, class, member, *etc.* with a particular
  group

