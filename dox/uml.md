UML For Chemists
================

This page is meant as a brief introduction to UML and also serves as a 
reference point for perusing the UML contained in this manual.

Contents
--------

- [Types of UML Diagrams](#types-of-uml-diagrams)
- [Use Case Diagrams](#use-case-diagrams)  
- [Activity Diagrams](#activity-diagrams)  
- [Sequence Diagrams](#sequence-diagrams)  
- [Class Diagrams](#class-diagrams)  

Types of UML Diagrams
---------------------

The UML standard specifies 13 different types of diagrams.  For our purposes we 
are primarily interested in the following four types:

- Use case diagram
  - Describe the features a system is expected to have
- Activity diagram
  - Describes the flow of control among components of a system
- Sequence diagram
  - Describes how classes interact
- Class diagram  
  - Details a class and its dependencies

This list of diagrams can be thought of as going from the most abstract to 
the most concrete in the sense that use case diagrams deals with enumerating 
broad functionality and classes are the entities that actually do the work.  
It should be noted that the content of one diagram is usually not orthogonal 
to that of another.  For example, sequence diagrams are typically written in 
terms of class methods, which of course also appear on the class diagrams. 


Use Case Diagrams
-----------------

Use case diagrams describe the "use cases" (services and functions) a package 
provides.  It also describes what type of users (called actors) will require 
each service.

In a use case diagram, the actors are depicted with stick figures labeled 
with their role in the diagram.  The things they are interacting with are 
modeled with rectangles and what they are doing is modeled with ovals.  
Actors are connected to their use cases via lines with no arrows.  Use cases 
are connected with arrows depicting their relationships.  Relationships come 
in two kinds "uses" (also known as "includes"), which indicates that a use 
case depends on another and "extends" which indicates that a use case is an
alternative option or generalization under certain conditions.  Respectively,
 these two relationships are denoted by an arrow with a solid tail and an 
 open head and an arrow with a dashed tail and head.


Activity Diagrams
-----------------

Activity diagrams depict the flow of control among components.  The starting 
point for flow is represented as a filled dot with an arrow pointing away 
from it.  Activities are connected with arrows, the direction depicting 
control flow, and each activity is represented by a rectangle with rounded 
edges.  When decisions influence control's flow, the decision is denoted with a
diamond.  Forking/joining of control flows is done with a horizontal line.  
The end point is shown with a filled circle embedded in a concentric open 
circle.

Sequence Diagrams
-----------------

Like activity diagrams, sequence diagrams depict control flow; however, 
unlike activity diagrams, sequence diagrams depict control flow among classes
 and not components.   

Class Diagrams
--------------

Class diagrams are used to depict the innards of a class as well as how that
class depends on other classes.  The overall diagram is static depicting 
things like inheritance, composition, *etc.* rather than call sequences or 
data passing.  The central components of a class diagram are classes.  
Classes are depicted as rectangles with three compartments. The top 
compartment is for the name of the class, the middle is for attributes, and 
the bottom is for member functions.  Visibility is denoted using a "+" for 
public, "#" for protected, and "-" for private.  Inheritance between classes 
is denoted with an arrow having a solid tail and an open head.  The arrowhead
points towards the base class.  Dependencies (when a class only depends on 
another class as an input/output type) are denoted by arrows having dashed 
tails; the arrowhead points towards the dependency.  Composition is when a 
class contains a member of another class and manages the lifetime of that 
member; composition is denoted with a filled diamond "arrowhead" the diamond 
is on the side opposite the member's type.  Finally, aggregation is when a 
class contains another class, but is not responsible for its lifetime (think 
shared pointers); this is depicted with an open diamond and again the diamond
is on the side opposite the member class.

In addition to representing class relationships, class diagrams are often 
used to represent relationships between components of the software package.  
Here folders are usually used for the components instead of the rectangles 
used for classes.  Again dependency arrows depict how the packages depend on 
one another. Composition relationships imply a package is contained 
within another.


References
----------

The contents of this page are distilled from [this](https://www.smartdraw.com/) 
website.  I refuse to pay for software, so UML diagrams were actually generated 
with [draw.io](http://draw.io/).
