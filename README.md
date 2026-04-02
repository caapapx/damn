# DeepSee - 智能技术调研与方案评估 Skill

一个置信度驱动的智能技术调研助手，通过科学方法驱动的调研流程，输出可行动的技术选型方案、竞品对标、创新建议、ROI评估。

## 功能特性

- **5阶段结构化流程**: 问题理解 → 数据源规划 → 执行调研 → 多角色分析 → 输出报告
- **3种工作模式**: 快速模式(≤8源) / 标准模式(≤15源) / 深度模式(≤25源)
- **置信度驱动**: 每项结论给出置信度(0-100%) + 证据更新轨迹
- **多角色协作**: 技术架构师、产品经理、成本分析师、行业分析师、CTO决策者
- **科学方法论**: 第一性原理、贝叶斯推理、辩证法、经济学思维

## 使用场景

- 技术选型决策（框架、数据库、云服务等）
- 竞品分析与对标
- 架构方案评估
- ROI与成本效益分析
- 技术可行性研究

## 测试结果

### 质量指标
- 所有测试用例通过率: 100%
- 覆盖场景: Dashboard技术选型、数据库选择、微服务迁移决策

### 效率指标
- 平均响应时间: 42.8s (比baseline快19%)
- Token使用: 19105 (比baseline少2%)
- 复杂场景提升明显: 微服务迁移决策快52%

## 目录结构

```
deepsee/
├── SKILL.md              # Skill定义文件
├── references/
│   ├── chart-playbook.md           # 图表选用与 Mermaid 模板（按需 Read）
│   ├── html-report-guide.md        # HTML 报告结构与样式约定
│   ├── deepsee-charts.example.json
│   └── report-data.example.json    # HTML 报告数据示例
├── scripts/
│   ├── install-global.sh
│   ├── uninstall-global.sh
│   ├── render_deepsee_charts.py    # 可选 PNG（matplotlib）
│   └── generate_html_report.py     # 交互式 HTML 报告
├── deepsee.md                      # 可选：与 SKILL 并行的长版说明（.gitignore）
├── evals/
│   └── evals.json       # 测试用例定义
├── tests/       # 测试结果
│   └── iteration-1/
│       ├── benchmark.json
│       ├── benchmark.md
│       └── [test-cases]/
└── README.md
```

## 安装使用

### 全局三平台（Cursor + Claude Code + Codex）

在本仓库根目录执行（会把当前仓库路径链到 `~/.agents/skills/deepsee`，再链到三端 skills；并安装 Claude 全局 `/deepsee`）：

```bash
./scripts/install-global.sh
```

装完后**重启** Cursor、Claude Code、Codex CLI。源目录保持为当前 clone（改 `SKILL.md` 或 `references/` 即全局生效，因符号链接指向本仓库）。

**卸载全局链接**（只删符号链接，**不删**本仓库）：

```bash
./scripts/uninstall-global.sh
```

卸载后同样建议重启各客户端。`~/.agents/skills/deepsee` 仅在符号链接解析到**当前仓库根目录**时才会删除；若你曾手动改指向其它路径，脚本会跳过并打印提示。

**可选图表**：见 `references/chart-playbook.md`；生成 PNG 需 `pip install matplotlib numpy` 后执行  
`python3 scripts/render_deepsee_charts.py -i references/deepsee-charts.example.json -o ./chart-out`。

**HTML 报告**：见 `SKILL.md` 阶段五与 `references/html-report-guide.md`；生成示例：  
`python3 scripts/generate_html_report.py -i references/report-data.example.json -o ./deepsee_report.html`（依赖以脚本内说明为准）。

### 项目内 / 手动

1. **Skill（自动触发）**：将含 `SKILL.md` 的 `deepsee/` 文件夹放入各工具的全局 skills 目录，或放入项目的 `.cursor/skills/` / `.claude/skills/`。
2. **Slash 命令（`/deepsee 你的问题`）**：将 `.claude/commands/deepsee.md` 复制到项目的 `.claude/commands/`；若已跑 `install-global.sh`，可使用用户级 `~/.claude/commands/deepsee.md`，任意仓库均可 `/deepsee …`。

仅一个 `SKILL.md` 对「行为说明」足够；若你要**和文档里一样的显式口令**，需要额外的 **command 文件**（上一条），二者分工不同，不是重复。

## 单文件会不会太简单？

不会。`SKILL.md` 已经包含完整五阶段流程、三档模式、工具策略与输出格式；复杂度在**流程与约束**，不在文件个数。可选扩展（按需再加文件即可）：`references/` 放模板或检查清单、`scripts/` 放辅助脚本、或按官方示例拆成多文件 skill——仅当维护或复用需要时再拆。

## License

MIT
