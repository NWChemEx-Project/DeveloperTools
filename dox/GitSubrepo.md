Git Subrepo Command
===================

It's natural to want to use other projects as dependencies of your project.  
Without git subrepos there are several ways to do this:

- Require the user to build the dependency manually
  - Somewhat silly for header-only or other non-compiled dependencies
  - Increases effort to use your project
  - Can be annoying for users due to version incompatibilities
- Copy/paste, put a tar-ball, *etc*. of the dependencies source code inside your
  project.
  - This is probably the worst option because:
    - Loose version control of dependency.
    - Git history stores entire source (bundle several versions of Boost with
      your repo and watch your clone's start taking forever).
- Assuming your project is under CMake, add the dependency as external_project
  - Again silly of header-only or other non-compiled dependency
  - Requires an internet connection to build (source downloaded at build time)
- Use git submodules 
  - "Canonical" git solution
  - Pain to use
    - Need to remember to always clone with `--recursive`
      - Forgetting to do this means needing to run 
        `git submodule update --init --recursive` for each submodule
    - Updating submodule is error-prone
      - Requires changes in two git repos (the parent repo and the dependency)
      - Easy to get into a messed-up history
- Use git subtrees
  - No enforced distinction between repos
  - Merging becomes complicated
     
Git subrepo [homepage](https://github.com/ingydotnet/git-subrepo) attempts to
provide a better solution than either submodules or subtrees.

Using Git Subrepo
-----------------

The documentation of the subrepo command is quite good.  The quick and dirty of
it is: 

Add a subrepo to your project:
~~~.git
#In root of your project
git subrepo clone <repo to add>
~~~

Update a subrepo:
~~~.git
#In root of your project
git subrepo pull <directory containing subrepo>
~~~

Contribute back to the subrepo's project:
~~~.git
#In root of your project
git subrepo push <directory containing subrepo>
~~~

Random Points to Note
---------------------

- Users of your project do not need subrepo command to use your repo
- Commits to a subrepo are part of the parent repo's history, unless you
  explicitly push them back to the subrepo.