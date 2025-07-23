#!/usr/bin/env bash
set -euo pipefail

KEY="$HOME/.ssh/cmsai-key"
REPO="git@github.com:deepdreamerfrommetaverse/cmsAI.git"
BRANCH="main"

# 1. Upewnij się, że jesteś w katalogu projektu
cd "$(dirname "$0")"

# 2. Zainicjuj repo, jeśli nie istnieje
if [ ! -d .git ]; then
  git init
  git checkout -b "$BRANCH"
else
  git checkout "$BRANCH" || git checkout -b "$BRANCH"
fi

# 3. Dodaj zdalne repo
if ! git remote | grep -q origin; then
  git remote add origin "$REPO"
fi

# 4. Dodaj wszystko i commit
git add -A
git commit -m "feat: force push full monorepo state" || echo "ℹ️  Nothing to commit."

# 5. Wypchnij z użyciem wskazanego klucza SSH
echo -e "\n🚀  Pushing to GitHub via SSH key: $KEY"
GIT_SSH_COMMAND="ssh -i $KEY" git push -f origin "$BRANCH"
