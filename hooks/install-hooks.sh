#!/bin/sh
# Install the G3 pre-commit hook into a project repo.
# Usage: sh hooks/install-hooks.sh /path/to/project-repo
set -e
REPO="${1:?usage: install-hooks.sh /path/to/project-repo}"
HOOK_SRC="$(cd "$(dirname "$0")" && pwd)/pre-commit"
HOOK_DST="$REPO/.git/hooks/pre-commit"
cp "$HOOK_SRC" "$HOOK_DST"
chmod +x "$HOOK_DST"
echo "G3 pre-commit hook installed at $HOOK_DST"
echo "Reminder: G3 is unwaivable. Bypassing with --no-verify is an X-class SEV1 waiting to be filed."
