#!/usr/bin/env bash
# 将本仓库以符号链接方式安装到 Cursor / Claude Code / Codex 全局 skills（及 Claude 全局 /damn 命令）
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENTS_SKILLS="${HOME}/.agents/skills"
mkdir -p "${AGENTS_SKILLS}" "${HOME}/.cursor/skills" "${HOME}/.claude/skills" "${HOME}/.codex/skills" "${HOME}/.claude/commands"
rm -rf "${AGENTS_SKILLS}/damn"
ln -sfn "${ROOT}" "${AGENTS_SKILLS}/damn"
ln -sfn "../../.agents/skills/damn" "${HOME}/.cursor/skills/damn"
ln -sfn "../../.agents/skills/damn" "${HOME}/.claude/skills/damn"
ln -sfn "../../.agents/skills/damn" "${HOME}/.codex/skills/damn"
ln -sfn "${ROOT}/.claude/commands/damn.md" "${HOME}/.claude/commands/damn.md"
echo "OK: damn -> ${ROOT}"
echo "  ~/.agents/skills/damn"
echo "  ~/.cursor/skills/damn  ~/.claude/skills/damn  ~/.codex/skills/damn"
echo "  ~/.claude/commands/damn.md"
echo "Restart Cursor / Claude Code / Codex after install."
