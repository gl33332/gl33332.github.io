#!/usr/bin/env bash
set -euo pipefail

# Hexo publish helper for Linux (replaces 发布并备份.bat)
# Flow:
#   1) git pull (ff-only)
#   2) bangumi update (best-effort)
#   3) hexo clean + generate
#   4) git add + commit (if changes)
#   5) print summary and STOP (no push)
# Then: user replies "发布" in Telegram, and we run scripts/push.sh

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

branch="${BRANCH:-master}"
remote="${REMOTE:-origin}"

step() { echo "\n==> $*"; }

step "[1/4] Sync repo: git pull --ff-only ${remote} ${branch}"
git pull --ff-only "$remote" "$branch"

step "[2/4] Bangumi update (best-effort): npx hexo bangumi -u"
if ! npx hexo bangumi -u; then
  echo "[!] bangumi update failed; continuing with local/cache data" >&2
fi

step "[3/4] Build: npx hexo clean && npx hexo generate"
npx hexo clean
npx hexo generate

test -f public/index.html || { echo "[!] Build did not produce public/index.html" >&2; exit 2; }

step "[4/4] Stage + commit (if needed)"
git add -A

if git diff --cached --quiet; then
  echo "No changes to commit."
else
  # Try to derive a semantic-ish commit message from changed paths
  msg="update: site"
  if git diff --cached --name-only | grep -q '^source/_posts/'; then
    changed_posts=$(git diff --cached --name-only | grep '^source/_posts/' | wc -l | tr -d ' ')
    msg="post: update ${changed_posts} file(s)"
  elif git diff --cached --name-only | grep -q '^_config'; then
    msg="config: update"
  elif git diff --cached --name-only | grep -q '^themes/'; then
    msg="theme: update"
  fi

  git commit -m "$msg"
fi

step "Summary (no push yet)"
echo "Branch: $branch"
echo
if git rev-parse --verify HEAD >/dev/null 2>&1; then
  echo "Last commit: $(git log -1 --oneline)"
fi

echo
echo "Changed files (working tree):"
git status --porcelain=v1 || true

echo
echo "Diff stat (last commit range):"
# If we created a commit, show last commit stats; else show staged stats is empty
if git diff --cached --quiet; then
  git show --stat --oneline -1 || true
else
  git diff --cached --stat || true
fi

echo
echo "READY_TO_PUSH=1"
