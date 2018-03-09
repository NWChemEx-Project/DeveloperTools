Organization of the NWChemEx-Project GitHub
===========================================

The purpose of this page is to explain how the NWChemEx's GitHub project is
arranged and to explain why these design decisions were pursued.

Monolithic Project vs. Many Tiny Libraries
------------------------------------------

Rather than having the entire NWChemEx package be a single GitHub repository the
decision was made to have each part be its own GitHub repository under the
NWChemEx-Project organization.  Particularly at the early development stage of
the project, there are numerous advantages to this approach including:

1. Components of the package are largely managed by teams to begin with
   - Facilitates mapping team leads to code bases
   - Pre-sorts pull-requests/issues
2. Simplifies testing
   - Each repository is responsible for testing itself and the integration of
   its subrepositories.
   - Avoids needing to retest all parts of the project for every PR (*e.g.* a
   change to coupled-cluster only needs to be tested by coupled-cluster and
   codes that depend on coupled-cluster.
3. Kernels will be able to largely stand on their own
   - Facilitates integrating kernels into other packages.
   - Easier to recognize people's contributions
4. On going development of a kernel need not influence other development
   - Since dependencies between kernels are managed by git can always use an
   old commit (*e.g.* a new SCF API doesn't have to be adopted by
   coupled-cluster immediately).  Particularly in prototyping phases an asset.
5. Building is easier
   -  Monolithic builds tend to be easiest with uniform build processes, which
   in turn makes it harder to customize the build of a particular library.

There are also some disadvantages:

1. Boilerplate
   - Similar build files, documentation, etc.  Presently the reason we use git
   subrepos.

The usage of many subrepositories is not meant to convey the notion that there
will not be an `NWChemEx` proper repo.  In fact there is (will be) one.


Proposed Workflow For Development
---------------------------------

1. Initialize the repo on GitHub
2. Clone it to your local box
3. Add `CMakeBuild` and `dox` as git subrepos
4. Develop your repo
5. Push back to your repo's GitHub repo

*N.B.* After the repository is created you really don't need the git subrepo
commands except to update dependencies.
