#!/usr/bin/env bash
set -euo pipefail

# Push helper. Use only after publish.sh printed READY_TO_PUSH=1 and user confirmed.
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

branch="${BRANCH:-master}"
remote="${REMOTE:-origin}"

echo "Pushing ${remote} ${branch}..."
git push "$remote" "$branch"
