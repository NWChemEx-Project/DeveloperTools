******************
How NWX's CI Works
******************

The purpose of this page is to document various aspects of NWX's CI.

CI Basics
=========

For the most part all of NWX's CI is run out of this repo. This is accomplished
by storing the workflows here and having the "Files Sync Action" synchronize
them across repos. The synchronization workflow is run out of
`.github/synch_files.yaml`.
