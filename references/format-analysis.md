# damn 报告格式分层说明

## 结论（现行）

采用 **三层可视化**（与 `presentation-widgets.md` / `SKILL.md` 展示总则一致）：

| 层 | 默认？ | 形态 | 目的 |
| --- | --- | --- | --- |
| **L0 对话态** | 是 | 决策卡、Markdown 表、Mermaid、置信度条 | Cursor / Codex / Claude 内一次性扫读 |
| **L1 归档态** | 否（用户要导出） | `generate_markdown_report.py` | Git 友好存档 |
| **L2 发表态** | 否（用户要 HTML/PNG） | HTML 生成器 / `render_damn_charts.py` | 分享、幻灯、打印 |

ASCII 柱图/框线 **不是** L0 默认；仅当宿主无法渲染 Mermaid 时作为流程 fallback，或用于极简成本条。

---

## 为何对话默认不做 HTML

1. **分发成本**：需浏览器打开，打断 agent 对话流  
2. **迭代差**：改结论要重新生成文件  
3. **企业环境**：部分环境打不开本地 HTML  
4. **决策需求**：对照表 + 一张流程图 normally 足够；精美图表边际收益低  

详见历史讨论：早期「HTML vs Markdown+ASCII」对比仍成立——**但 ASCII 图表库已降级为 fallback**，主路径改为表 + Mermaid。

---

## L0 必须有的扫读面

1. 开篇决策卡（结论 / 权重矩阵 / 置信度）  
2. 阶段二探测卡（表，非 doctor 长行）  
3. 证据账本或行内 Lx  
4. 工作流 Mermaid（标准/深度）  

清单与门禁：`presentation-widgets.md`、`quality-gates.md` → Presentation gate。

---

## L1 / L2 何时

仅当用户明确说「导出报告 / 归档 / HTML / PNG」：

1. 数值必须来自已完成调研 JSON（禁止填模板编造）  
2. Markdown：`scripts/generate_markdown_report.py`  
3. HTML：`scripts/generate_html_report.py` + `html-report-guide.md`  
4. PNG：`chart-playbook.md` + `render_damn_charts.py`  
