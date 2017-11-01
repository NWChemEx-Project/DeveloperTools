Git and GitHub Procedures
=========================

The purpose of this page is to document typical git and GitHub workflows and to
serve as a cheat sheet for remembering commands.  This page only covers the 
aspects related to basic version control under git and how to contribute code.

Contents
--------

1. [Git and GitHub Background](#git-and-github-background)
2. [Common Git Commands](#common-git-commands)
3. [GitHub Workflow](#github-workflow)

Git and GitHub Background
-------------------------

Git is a version control (VC) program similar to Mercurial, CVS, and SVN.  
Like most VC programs git manages a code base called a repo.  To work on a 
code a developer checks out the repo (called cloning in git lingo), modifies 
the resulting local copy, and then saves the changes (called committing). The
primary differences among the various VC programs is whether or not they 
adopt a centralized or a distributed repo model.  In the centralized model, 
there is only one authoritative repo (call it the master repo).  All 
operations, like committing and cloning, require synchronization with 
the master repo.  In contrast, in the distributed model each repo is a full 
fledged repo and can be treated as the master repo.  Under this model, any 
"authoritative" repo is purely social convention.  This leads to a number of 
advantages compared to centralized repos:

- Faster operations
  - No remote communication necessary
- Easy collaboration
  - Can pull/push with any other repo, not just master repo
- Each repo is essentially a "back-up"  

GitHub is a website for hosting git repos.  To some extent that's all it is, a
place to put a repo.  As it relies on git, there's nothing special about the 
repo living on GitHub versus a clone living on another computer.  That said 
it's conventional to, by social convention, treat the GitHub repo as the 
"official" repo.  Another nice aspect of GitHub is that it provides 
extensions to git that are possible because of the fact that it is a website.
The following sections detail common git commands as well as the GitHub 
workflow.

Common Git Commands
------------------- 

For the moment we'll assume that you're going to be working with an existing 
git repo.  To that end we'll ignore how to setup a git repo.  In this case, the
first step is for you to get your own copy of the project you want to work on
.  The command is:

~~~.git
git clone <path_to_repo> [<where_to_put_repo>]
~~~

This will checkout a repo that is located at `path_to_repo` and optionally 
put it at `where_to_put_repo` (if you don't specify where to put it, it goes 
in the current directory in a folder named the same as the repo you are 
cloning).  It's important to realize that `path_to_repo` can be either a file
path, to say clone a repo on your internal network, or a website like GitHub.
The remainder of the commands in this section assume you are inside the 
resulting directory (git will try to access settings that are hidden in `
.git/` folders and will complain if said folders don't exist).

By default the repo you get only has the master branch (*i.e.* the branch 
representing the non-in-development code).  It's best to keep this branch clean
(*i.e.* the same as that of the repo you cloned) as it'll make your life 
easier when it comes time to get updates and to merge.  To this end the first
thing you should do is make a new branch.  This is done by:

~~~.git
git checkout -b <branch_name>
~~~

where `branch_name` is the name of the branch you'll be working on.  In general
you should have one branch per feature you're working on.  So now time goes by
and you've written code and want to save that code's state so you can revert to
it if something goes horribly wrong.  First you have to tell git what code you
want to save:

~~~.git
git add <files_to_save>
~~~

Note that at this point the files are not saved (they are what is typically 
referred to as staged).  The staging phase makes it easier for you to fine tune
what gets saved and what doesn't.  You can run `git add` as many times as you
want to keep building up the staged file list.  At this point it's useful to 
note that you can see which files are staged, which files are changed, and 
which files exist (but are not under git control) via:

~~~.git
git status
~~~  

Once you're happy with the set
of files to save, you commit them via:

~~~.git
git commit -m "<message>"
~~~

This command will save all staged files to your branch.  You can now, at a later
point in time return to this code state if you so choose.  Note that the files
are only saved to your current branch, they are not saved to any other branch
yet.  To contribute them back to another repo you "push" your changes. As 
this tutorial is aimed at working within the typical GitHub workflow we'll 
worry about saving to other branches there.  For now it's useful to make
note of several other git commands.

When collaborating on a project it is almost inevitable that someone else will
commit code to the repo you're also developing for (*i.e.* the master branch 
of your repo will be behind that of the repo you cloned).  To synchronize 
them (assuming you're on your development branch and not master), first change
to your master branch:

~~~.git
git checkout master
~~~

and then obtain ("pull" in git parlance) the original repo's master branch via:

~~~.git
git pull origin master
~~~

This command will take the copy of the master branch stored in the repo 
"origin" (when you clone a repo git automatically assigns an alias to that 
repo called origin, you could alternatively type out the path/url again) and 
merge it into your local master branch.  Since you're following this tutorial
there'll be no problems with the merge and everything will go swimmingly.  
With your master branch up-to-date you'll want to merge those changes into 
your active development branch (you won't be able to contribute back 
otherwise).  To do this, check-out your development branch and run:

~~~.git
git merge master
~~~

This will merge the contents of your master branch into your current branch. 
 It is possible for conflicts to occur at this point, so it's worth 
 discussing them now.  Git's pretty good about merging 
contributions from multiple developers.  Nevertheless conflicts occur.  If 
during a merge a conflict does occur, you'll have to correct it manually. To 
do this take note of the conflicting files (if you forget you can get the 
list again by running `git status`).  For each file you'll
need to fix all conflicts contained within it.  Git will fence-off the 
conflicting lines of code by `<<<<<<< HEAD` and `>>>>>>> BRANCH-NAME` 
delimiters (`BRANCH-NAME` will be descriptive of ).  The top section (relative
 to the 
`=======` 
delimiter) will
 be 
your file, the bottom will be 
 the one that is merging into your file.  You'll need to delete the 
 delimiters and fix the code.  Once you've done that you stage and commit the
  file.
  
GitHub Workflow
---------------

The above commands are complemented by several GitHub exclusive extensions.  
Let's say you want to contribute to a very creatively named repo on GitHub 
called "GitHubRepo".  Well we've got two problems.  First, the maintainers of
"GitHubRepo" probably don't want you directly committing to their code 
base without them first looking at your contribution ("looking at" is 
typically automated to some extent).  Hence, they'll need to pull your changes 
into a sandbox area and assess them before committing them.  This is the 
second problem, you probably don't want them accessing your computer. GitHub has 
purposed a solution, it's called forking.  Alls it is, is a fancy clone 
procedure.  During forking GitHub clones "GitHubRepo" to your account (thereby 
hosting the clone on GitHub itself).  We'll call the resulting clone 
"GitHubFork". Basically "GitHubFork" is a buffer repo that you both can 
access comfortably (as in the spirit of git itself each fork is a legitimate 
GitHub repo on it's own and can be forked too, great for collaborations on 
contributions).  As for how to fork, on "GitHubRepo"'s GitHub page just click 
the fork button at the top.

After forking the git procedure continues like normal.  You clone 
"GitHubFork" to your local machine and checkout a new branch preserving 
master.  To save yourself a lot of headaches later you'll want to define an 
alias for "GitHubRepo".  Typically this alias is called "upstream".  To make 
this alias the command is:

~~~.git
git remote add upstream <path_to_original_repo>
~~~

It is polite at this point to notify the maintainers of "GitHubRepo" that you're
going to work on this feature.  To do this you first push your development 
branch to "GitHubFork".  Then on "GitHubFork"'s GitHub page you should see a 
box pop up that says your branch's name and "compare and pull request" (if 
not you can go to the branches tab and manually start a pull request).  A 
pull request is just that, it's a request for the maintainers of "GitHubRepo" to
pull the specified branch into their repository.  Since you're opening this 
PR (that's short for pull request and is a very prevalent abbreviation on 
GitHub, so learn it) before finishing the code it's customary to title the PR 
something like "[WIP] Descriptive Title".  Here "WIP" stands for "work in 
progress" (again common abbreviation) and tells the maintainers that it's not
ready yet.  You'll also need to provide a description of what your feature 
does (many repos will provide a template that you should fill out to the best
of your ability).  Starting the PR early is a good idea as it provides you a 
means of getting feedback along the way ranging from "don't bother doing 
this, we don't want your feature" to "that's great, let us know if there's 
any way we can help you get that implemented".  It also will be the place 
where a code review (the maintainers of the repo look at your code and make 
comments on it) will occur.  By starting early the code-review can be done in
stages (assuming you regularly update "GitHubFork").

For the most part the remainder of the development cycle is pretty 
standard.  The big exception is staying synchronized with "GitHubRepo".  Since 
other developers who contribute to "GitHubRepo" aren't going to be nice
enough to push their changes to your fork of the repo, you can't just run the
pull command from the last section.  Hence, in order for you to stay
up-to-date with "GitHubRepo" you'll need to pull changes from it's master 
branch into your local master branch.  The command is similar (and the reason
we defined the "upstream" alias):

~~~.git
git pull upstream master
~~~

With your local master branch synched, you'll then want to synch 
"GitHubFork"'s master branch.  To do this you'll push the local changes to 
"GitHubFork".  The command is:

~~~.git
git push origin master
~~~

Although not strictly necessary, this step makes it easier for you to recover
should anything go wrong.  In particular if you accidentally modify your 
local master branch you may get conflicts while synchronizing.  By ensuring your
"GitHubFork" master branch is a clean copy of the "GitHubRepo"'s at some 
point in its history you can run:

~~~.git
git reset --hard origin/master
~~~

This command will delete all changes made to the current branch, and make it 
exactly equal to the state of "GitHubFork"'s master branch.  YOU WILL ALMOST 
CERTAINLY LOOSE WORK BY DOING THIS.  It's thus best to first checkout a new 
branch, that is a copy of the current branch, before executing this command.  

Once you're done developing you need to notify the "GitHubRepo" maintainers. 
This is typically done in two ways.  First, the "[WIP]" tag is removed from 
the title of your PR.  As this easy to miss, you typically will also comment in 
the PR "r2g" (short for ready to go).  Comments are a lot harder to miss.  At
this point the ball's in the maintainers court to accept your PR or provide 
additional feedback of things that need fixing (which assuming you were 
pushing to "GitHubFork" regularly, will hopefully not be a long list).  Once 
the PR is approved either you or the maintainers will click on the "merge" 
button provided by GitHub and your code will be merged. At this point the PR 
is closed and you can delete your branch.  It is recommended that the 
contributor clicks merge in order to avoid premature merging (simply because 
the reviewer has accepted what's there doesn't mean that the contributor is 
done contributing via that PR). 


 
