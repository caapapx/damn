#!/usr/bin/env bash
# Install to ~/.claude/skills (Cursor + Claude Code) and ~/.kimi/skills (Kimi Code).
# Prefer skill-manager's link-user-skill.sh when this tree is nested; otherwise hop locally.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="damn"

find_link_helper() {
  local d="$ROOT"
  while [[ "$d" != "/" ]]; do
    if [[ -x "${d}/scripts/link-user-skill.sh" ]]; then
      echo "${d}/scripts/link-user-skill.sh"
      return 0
    fi
    d="$(dirname "$d")"
  done
  return 1
}

if helper="$(find_link_helper)"; then
  bash "${helper}" "${ROOT}" "${NAME}"
else
  mkdir -p "${HOME}/.claude/skills"
  ln -sfn "${ROOT}" "${HOME}/.claude/skills/${NAME}"
  if [[ -d "${HOME}/.kimi" ]]; then
    mkdir -p "${HOME}/.kimi/skills"
    ln -sfn "${ROOT}" "${HOME}/.kimi/skills/${NAME}"
  fi
  # Avoid Cursor double-load
  for hop in "${HOME}/.cursor/skills/${NAME}" "${HOME}/.agents/skills/${NAME}" "${HOME}/.codex/skills/${NAME}"; do
    [[ -L "${hop}" ]] && rm -f "${hop}" || true
  done
  echo "OK: ${NAME} -> ${ROOT} (standalone hop; skill-manager link helper not found)"
fi

mkdir -p "${HOME}/.claude/commands"
ln -sfn "${ROOT}/.claude/commands/damn.md" "${HOME}/.claude/commands/damn.md"
echo "  ~/.claude/commands/damn.md"
echo "Restart Cursor / Claude Code / Kimi Code after install."
