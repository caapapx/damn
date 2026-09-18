# DAMN Toolchain Matrix

新机可以跑 damn 的五阶段协议；外置检索/社区能力是增强层，不是硬依赖。
本表供 `scripts/doctor.sh` 与阶段二能力规划共用。

## 分级

| 级 | 含义 | 缺失时 |
| --- | --- | --- |
| **required_host** | 由 Cursor / Claude 等宿主提供 | 换宿主或开 MCP；doctor 只能标注 `host_assumed` |
| **required_local** | 本机命令，跑 skill 自带脚本需要 | 安装后重跑 doctor |
| **optional_enhance** | 加深搜索/社区/爬取 | 回退 WebSearch / WebFetch / 官方 API；披露缺口 |
| **optional_export** | 报告导出美化 | 跳过 PNG/HTML 增强，用 Markdown |

## 矩阵

| 能力 | 级 | 探测信号 | 凭证（只查有无，不回显） | 回退 |
| --- | --- | --- | --- | --- |
| Agent 宿主（对话 + 工具） | required_host | 会话本身 | — | 无法在 shell 代偿 |
| 宿主网页搜索 / Fetch / MCP | required_host | 宿主工具列表 | MCP OAuth 由宿主管 | 用户粘贴 URL / 本地文件 |
| `python3` | required_local | `command -v python3` | — | 无法跑 validate / 报告脚本 |
| `curl` | required_local | `command -v curl` | — | 宿主 WebFetch |
| Agent Reach | optional_enhance | `agent-reach doctor --json` | 各渠道登录态 | 现有 Web/MCP；见 `capability-routing.md` |
| GitHub CLI `gh` | optional_enhance | `gh auth status` | `gh` 登录 | GitHub MCP / raw.githubusercontent.com |
| Firecrawl CLI | optional_enhance | `command -v firecrawl` | `FIRECRAWL_API_KEY` 或 CLI 登录 | WebFetch |
| Brave Search | optional_enhance | env | `BRAVE_API_KEY` | 其他搜索适配器 / 宿主搜索 |
| Exa | optional_enhance | env | `EXA_API_KEY` | 同上 |
| Tavily | optional_enhance | env | `TAVILY_API_KEY` | 同上 |
| matplotlib + numpy | optional_export | `python3 -c "import matplotlib,numpy"` | — | 纯 Markdown / 跳过 PNG |

## 策略（硬约束）

1. **默认 `/damn` 只探测、不安装。** 安装必须用户显式跑 doctor 的 `--install …` 或手工执行建议命令。
2. **不自动登录、不读写 Cookie、不打印 Token 值。** 密钥检查只输出 `set` / `unset` / `invalid_shape`。
3. **最佳状态** = required_* 全绿 + 你常用的 optional_enhance 为 `ok`；不是「装齐矩阵每一行」。
4. Agent Reach / 付费搜索的安装与账单以各工具自己的文档为准；damn 只给建议命令，不代付、不代注册。
5. **外网调研阶段二必须先探测**（本脚本或宿主 MCP 清单）。探测结果里只有 Firecrawl 等单一搜索/爬取通道时，仍须遵守 `source-routing.md` Hard gates（`single_adapter_reason` + 深读优先 WebFetch），不得把「矩阵里有 Firecrawl」理解成全局 primary。

## 相关文件

- 探测脚本：`scripts/doctor.sh`
- 渠道路由：`capability-routing.md`
- 搜索适配：`source-routing.md`
- 运行时能力对象：`harness-contract.md` → `CapabilityProfile`
