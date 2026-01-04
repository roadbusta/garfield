#!/usr/bin/env bash
set -euo pipefail

SOURCE="/Users/joe/Library/Caches/com.apple.findmy.fmipcore/Items.data"
REPO_DIR="/Users/joe/Desktop/code/garfield"
DEST_DIR="data"
BRANCH="main"

while true; do
  cd "$REPO_DIR"

  git checkout "$BRANCH" >/dev/null 2>&1 || git checkout -b "$BRANCH"
  git pull --rebase origin "$BRANCH"

  timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
  DEST_RELATIVE_PATH="$DEST_DIR/file_${timestamp}.txt"

  mkdir -p "$DEST_DIR"
  cp "$SOURCE" "$DEST_RELATIVE_PATH"

  git add "$DEST_RELATIVE_PATH"

  msg="Auto update $(date '+%Y-%m-%d %H:%M:%S')"
  git commit -m "$msg"
  git push origin "$BRANCH"

  sleep 900
done