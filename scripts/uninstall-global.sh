#!/usr/bin/env bash
# 撤销 install-global.sh 写入的全局符号链接（不删除本仓库目录）
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

remove_if_symlink() {
  local target=$1
  if [[ -L "$target" ]]; then
    rm -f "$target"
    echo "removed: $target"
  elif [[ -e "$target" ]]; then
    echo "skip (not a symlink): $target"
  fi
}

echo "damn global uninstall (symlinks only, repo at ${ROOT} is kept)"
remove_if_symlink "${HOME}/.claude/commands/damn.md"
remove_if_symlink "${HOME}/.cursor/skills/damn"
remove_if_symlink "${HOME}/.claude/skills/damn"
remove_if_symlink "${HOME}/.codex/skills/damn"

# 主链接：仅当指向本仓库时才删，避免误删你手动改到别处的 ~/.agents/skills/damn
agents_damn="${HOME}/.agents/skills/damn"
if [[ -L "$agents_damn" ]]; then
  resolved=$(readlink -f "$agents_damn" || true)
  root_resolved=$(readlink -f "$ROOT" || true)
  if [[ -n "$resolved" && "$resolved" == "$root_resolved" ]]; then
    rm -f "$agents_damn"
    echo "removed: $agents_damn"
  else
    echo "skip: $agents_damn -> $resolved (not this repo at $root_resolved)"
  fi
elif [[ -e "$agents_damn" ]]; then
  echo "skip (not a symlink): $agents_damn"
fi

echo "Done. Restart Cursor / Claude Code / Codex if they were using this skill."
