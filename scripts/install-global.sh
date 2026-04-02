#!/usr/bin/env bash
# 将本仓库以符号链接方式安装到 Cursor / Claude Code / Codex 全局 skills（及 Claude 全局 /deepsee 命令）
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENTS_SKILLS="${HOME}/.agents/skills"
mkdir -p "${AGENTS_SKILLS}" "${HOME}/.cursor/skills" "${HOME}/.claude/skills" "${HOME}/.codex/skills" "${HOME}/.claude/commands"
# 迁移：移除旧 damn 链接或目录
ln -sfn "${ROOT}" "${AGENTS_SKILLS}/deepsee"
ln -sfn "../../.agents/skills/deepsee" "${HOME}/.cursor/skills/deepsee"
ln -sfn "../../.agents/skills/deepsee" "${HOME}/.claude/skills/deepsee"
ln -sfn "../../.agents/skills/deepsee" "${HOME}/.codex/skills/deepsee"
ln -sfn "${ROOT}/.claude/commands/deepsee.md" "${HOME}/.claude/commands/deepsee.md"
echo "OK: deepsee -> ${ROOT}"
echo "  ~/.agents/skills/deepsee"
echo "  ~/.cursor/skills/deepsee  ~/.claude/skills/deepsee  ~/.codex/skills/deepsee"
echo "  ~/.claude/commands/deepsee.md"
echo "Restart Cursor / Claude Code / Codex after install."
