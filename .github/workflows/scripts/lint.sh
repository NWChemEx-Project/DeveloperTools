#!/bin/sh

# Wraps the process of running clang-format on the source code
#
# Usage:
#   lint [<dir2lint1> [<dir2lint2> [...]]]
# Optional Arguments:
#   dir2lint1: Path (either absolute or relative) to the first directory to
#              lint. Contents will be linted in place.
#   dir2lint2: Path (either absolute or relative) to the second directory to
#              lint. Contents will be linted in place.
clang_formart_cmd="clang-format-9"
for dir2lint in "$@"; do
  find "${dir2lint}" -name '*.hpp' -or -name '*.cpp' | \
  xargs "${clang_format_cmd}" -style=file -i -fallback-style=none
done
