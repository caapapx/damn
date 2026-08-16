# 互联网证据能力路由

本参考把 Agent Reach 当作可选的“能力层”：它负责为部分互联网渠道选择当前可用的接入方式，damn 仍负责证据规划、分级、交叉验证与决策。不要把 Agent Reach 的具体后端命令复制进本 skill；上游会替换后端，运行时体检结果才是事实。

## 路由矩阵

| 证据任务 | 可回答的问题 | 首选证据 | Agent Reach 前提 | 回退路径 | 不能推出 |
| --- | --- | --- | --- | --- | --- |
| 网页/官方资料 | 当前规格、文档、发布说明是什么 | 官方页面或标准正文 | Web channel `ok` | WebFetch、官方 API | 页面可访问不等于内容正确 |
| GitHub | 项目实现、Issue、Release、维护活动 | 仓库源码、官方 Issue/Release | GitHub channel `ok` | GitHub 官方网页/API/MCP | Star/fork 数不等于质量 |
| 全网搜索 | 候选方案与近期变化有哪些 | 多源搜索结果，再回到原文 | 搜索 channel `ok` | WebSearch、搜索 MCP | 搜索摘要不是证据本体 |
| Reddit/X/V2EX | 真实问题、迁移障碍、采用体验 | 多个独立讨论，回链原帖 | 目标社区 channel `ok` 且登录态已由用户准备 | 公开网页、官方 issue、公开案例 | 热度不能代表市场、质量或性能 |

## 执行契约

1. 只有规划确实需要该渠道时才探测：运行 `agent-reach doctor --json`，只读取目标渠道的 `status`、`active_backend`、`message` 和 `backends`。
2. `status=ok` 才按运行时后端执行；`warn`、`off`、`error` 必须转入回退路径。不要仅凭命令存在、配置文件存在或历史经验宣称可用。
3. 每条结果写入最小账本：`channel`、`backend_or_fallback`、`query_or_url`、`collected_at`、`evidence_level`、`limitations`。
4. 社区内容默认是 L3/L4 代理证据。只有能回溯到用户提供的可复现日志或受控实验，才可升级为 L1；不能因多人重复转述就升级。
5. Agent Reach 不是安装器：damn 不自动安装依赖、不自动登录、不提取/注入 Cookie、不在输出和日志中打印 Token、Cookie、Authorization header 或完整敏感 URL。

## 通用失败链

```text
未安装 agent-reach
  -> 使用现有 Web/MCP/官方来源
渠道未配置或未登录
  -> 不绕过认证；改用公开来源，并在置信度中披露缺口
后端体检通过但采集失败
  -> 记录错误与实际后端；尝试既有工具或另一证据类型
超时、限流、内容不可复验
  -> 保留已获来源；降低该证据组权重；给出最小补证动作
```

## 输出示例

```text
来源：GitHub Issue #123
渠道：github
实际路径：Agent Reach doctor=ok，后端由运行时返回
采集时间：2026-08-04T...
证据级别：L2（公开一手项目材料）
局限：仅代表维护者/参与者讨论，不证明全体用户体验
```
