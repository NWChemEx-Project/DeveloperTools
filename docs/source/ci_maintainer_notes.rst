******************
How NWX's CI Works
******************

The purpose of this page is to document various aspects of NWX's CI.

File Synchronization
====================

There are several files which need to appear in each NWX repo and whose content
doesn't change. This includes:

- .clang-format
- .gitignore
- LICENSE

Rather than remembering to update these files in each repo anytime they need to
change, we rely on the
`Files Sync Action<https://github.com/marketplace/actions/files-sync-action>`_
to keep them synchronized.
