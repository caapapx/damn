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

echo "DeepSee global uninstall (symlinks only, repo at ${ROOT} is kept)"
remove_if_symlink "${HOME}/.claude/commands/deepsee.md"
remove_if_symlink "${HOME}/.cursor/skills/deepsee"
remove_if_symlink "${HOME}/.claude/skills/deepsee"
remove_if_symlink "${HOME}/.codex/skills/deepsee"

# 主链接：仅当指向本仓库时才删，避免误删你手动改到别处的 ~/.agents/skills/deepsee
agents_deepsee="${HOME}/.agents/skills/deepsee"
if [[ -L "$agents_deepsee" ]]; then
  resolved=$(readlink -f "$agents_deepsee" || true)
  root_resolved=$(readlink -f "$ROOT" || true)
  if [[ -n "$resolved" && "$resolved" == "$root_resolved" ]]; then
    rm -f "$agents_deepsee"
    echo "removed: $agents_deepsee"
  else
    echo "skip: $agents_deepsee -> $resolved (not this repo at $root_resolved)"
  fi
elif [[ -e "$agents_deepsee" ]]; then
  echo "skip (not a symlink): $agents_deepsee"
fi

echo "Done. Restart Cursor / Claude Code / Codex if they were using this skill."
