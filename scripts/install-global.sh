#!/usr/bin/env bash
# Install to ~/.claude/skills (Cursor + Claude Code) and ~/.kimi/skills (Kimi Code).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SM="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
bash "${SM}/scripts/link-user-skill.sh" "${ROOT}" "damn"
mkdir -p "${HOME}/.claude/commands"
ln -sfn "${ROOT}/.claude/commands/damn.md" "${HOME}/.claude/commands/damn.md"
echo "  ~/.claude/commands/damn.md"
echo "Restart Cursor / Claude Code / Kimi Code after install."
