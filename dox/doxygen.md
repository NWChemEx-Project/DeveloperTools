Using Doxygen in the NWChemEx Project
=====================================

The purpose of this page is to give you a (likely less than 10 minute) primer on
how to use Doxygen particularly with respect to the NWChemEx project.

Contents
--------

- [Documenting Code](#documenting-code)
  - [Intro to Doxygen](#intro-to-doxygen)
  - [Minimal Standards](#minimal-documentation-standards)
- [Documentation Pages](#documentation-pages)

Documenting Code
----------------

The point of this section is to get you acquainted with the basic aspects of 
Doxygen, such as how to to document the code and the basic commands to do so.
Also in this section you will find our minimal documentation standards.  You 
can always write more documentation, but these define the bare minimum. 

### Intro To Doxygen 

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
conventions for the NWChemEx project.  For consistency please use them.

Already, this simple example has demonstrated the two main types of 
documentation in Doxygen: brief and detailed.  Brief documentation, as the 
name implies, is meant to quickly convey what a function or class does.  For 
example, [this link](https://codedocs.xyz/doxygen/doxygen/annotated.html) 
shows the brief descriptions for the classes inside Doxygen itself (yes 
Doxygen is documented using Doxygen).  As you can see the descriptions are 
short and should fit on one line.  If you click on one, say the ClassDef 
class, you'll get taken to a page showing the details of the class.  On that 
page you can now read the detailed description of the class [link to said 
description](https://codedocs.xyz/doxygen/doxygen/classClassDef.html#details)
.  The detailed description is (in this case not that much) more detailed and
 typically provides details a user would need to know to use the class 
 (instead of just what the class does).
 
 By convention the single line comments are always briefs, whereas the first 
 line (up to the first period)of a multi-line comment is the brief and the 
 remaining lines are the detailed description.  When making multi-line comments
 it is good practice to start the brief with `@brief`.  This will ensure that
 the brief continues until the first blank line and will prevent surprises from
 forgetting the period convention.  `@brief` is an example of a Doxgyen 
 keyword.  Keywords are signaled by the `@` symbol (there's another 
 convention too, but this is the one approved for NWChemEx).  There's a lot of
 keywords, a full list of them is available 
 [here](http://www.stack.nl/~dimitri/doxygen/manual/commands.html).  The next
 section gets you acquainted with the minimum set you know.  Again, feel free
 to learn others and use them.


### Minimal Documentation Standards

By far the most useful keywords are shown in the following code example.  For
 documenting a function this should be considered as a minimal acceptable 
 amount of documentation.  For documenting data members and types a single line
 comment is often fine (just describing what it is).

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
 the key things to document: brief, detailed description, input/output 
 parameters, return value, template type (or non-type) parameters, and 
 exceptions that are thrown (as well as the level of exception guarantee).
 
 Other useful commands to be aware of:
- `@file` for documenting files
  - Should be particularly used when a file contains more than just a class
- `@defgroup` used to define groups for organizational reasons
- `@ingroup` for associating a file, class, member, *etc.* with a particular
  group
- `@f$<latex here> @f$` for adding on line Latex formulae
- `@f{eqnarray}{` for starting a Latex eqnarray (obviously change the 
   environment name to get other environments)
   - This environment is ended by `@f}`
- `@note` for starting a note
- `@todo` for adding something to the TODO list
- `@warning` for displaying a warning to the reader
- `@bug` for letting the reader know about a known bug
- `@relates` for free-functions really designed to be used with a class 
ensures the documentation for the function is with the class.      

Documentation Pages
-------------------

Doxygen supports the inclusion of pages (like this one) in your documentation
for discussing involved topics.  These are pages that either don't specifically
relate to any one piece of code (like this one) or explain in detail
how to use a class or function (typically with a plethora of examples).  
Regardless of their purpose these pages live in the `dox` directory of your
project and need to be added to the `settings.doxcfg` file.  Historically these
pages had to be written within a C++ comment block.  Nowadays they can be 
markdown (like this page).  What's cool about the latter is that means 
they'll display pretty on GitHub too.

Documentation pages are free form in the sense that they can contain a mix of
markdown and Doxygen commands (*N.B.* that means you can put Latex equations 
in them...).  That said GitHub won't render Doxygen commands and it is best to
only use them when you need them.  Long term the plan is to make the generated
Doxygen the authoritative documentation source; however, this is really 
facilitated by automatic documentation builds, which we can't do until the repo
is public.
