Organization of the NWChemEx-Project on GitHub
==============================================

One of NWChemEx's core concepts is striving to achieve a strongly decoupled code
base. This facilitates code resuse from other projects and promotes the
incorporation of NWChemEx's modules into other packages. To this end we have
made each major component of NWChemEx into its own separate repository under the
NWChemEx-Project GitHub organization.

So Where's "NWChemEx"?
----------------------

Having a bunch of individual repos is great for developers, but confusing to
users. For this reason we have a convenience repo ``NWChemEx-Project/NWChemEx``.
Users who want the whole NWChemEx experience should clone this repo and build
it. This repo will automatically pull and build the rest of the repos required
to produce a complete NWChemEx "binary".

Repositories
------------

This section lists the current NWChemEx repositories and provides a brief
description of what each repository does. Roughly speaking the repositories can
be thought of as belongin to one of two groups. The first group focuses on the
code itself. These repos contain the actual source code used to produce NWChemEx
and its modules. The following table lists these core repos from the most l
ow-level to the most top-level.

============== ===================================================
Repository     Description
============== ===================================================
Utilities      Helpful, generic C++ classes akin to Boost/STL
TaskForce      The runtime abstraction layer
SDE            The runtime framework
TAMM           A C++ tensor library designed for quantum chemistry
LibChemist     Chemistry specific classes
PropertyTypes  Definitions of the module APIs
Integrals      Modules implementing AO-based integrals
SCF            Modules implementing self-consistent field theory
MP2            Modules implementing MP2 (and variations of it)
CoupledCluster Modules implementing coupled cluster theory
NWChemEx       Top-level, user-centric repo for getting everything
============== ===================================================

The remaining repositories owned by the NWChemEx-Project are meta repositories.
Some of these repos are private (and will remain private) so their visibility to
a reader will depend on that reader's membership with the NWChemEx-Project. In
no specific order these repos are:

============== ==========================================================
Repository     Description
============== ==========================================================
DeveloperTools Developer documentation and tools for maintaining NWChemEx
Publications   Manuscripts written by the NWChemEx team about NWChemEx
dox            Deprecated documentation repo
CMakeBuild     Deprecated build system
============== ==========================================================
