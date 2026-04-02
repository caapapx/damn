#!/usr/bin/env python3
"""
DeepSee Markdown 报告生成器 - 使用 ASCII 图表
用法: python3 generate_markdown_report.py -i report_data.json -o report.md
"""
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

def ascii_bar_chart(data: dict, width: int = 40) -> str:
    """生成 ASCII 柱状图"""
    title = data.get('title', '')
    categories = data.get('categories', [])
    values = data.get('values', [])
    max_val = max(values) if values else 1

    lines = [f"\n{title}\n"]
    for cat, val in zip(categories, values):
        bar_len = int((val / max_val) * width)
        bar = '█' * bar_len + '░' * (width - bar_len)
        lines.append(f"  {cat:12} │{bar}│ {val}")
    return "\n".join(lines)

def ascii_heatmap(data: dict) -> str:
    """生成 ASCII 热力图"""
    title = data.get('title', '')
    rows = data.get('rows', [])
    cols = data.get('cols', [])
    values = data.get('values', [])

    # 色块映射
    def get_block(val):
        if val >= 8: return '█'
        elif val >= 6: return '▓'
        elif val >= 4: return '▒'
        else: return '░'

    lines = [f"\n{title}\n"]
    # 表头
    lines.append("       " + "  ".join([f"{c:6}" for c in cols]))
    # 数据行
    for i, row in enumerate(rows):
        blocks = "".join([f" {get_block(values[i][j])} " for j in range(len(cols))])
        lines.append(f"{row:6} {blocks}")
    lines.append("\n图例: █=9-10  ▓=7-8  ▒=5-6  ░=0-4\n")
    return "\n".join(lines)

def ascii_line_chart(data: dict, height: int = 10) -> str:
    """生成 ASCII 折线图"""
    title = data.get('title', '')
    labels = data.get('labels', [])
    values = data.get('values', [])

    if not values:
        return ""

    max_val = max(values)
    min_val = min(values)
    range_val = max_val - min_val if max_val > min_val else 1

    lines = [f"\n{title}\n"]

    # Y 轴标签
    for y in range(height, -1, -1):
        val = min_val + (y / height) * range_val
        line = f"{val:6.0f} │"

        # 绘制数据点
        for x, v in enumerate(values):
            normalized = (v - min_val) / range_val if range_val > 0 else 0
            if abs(normalized * height - y) < 0.5:
                line += "●"
            elif y == 0:
                line += "─"
            else:
                line += " "
            line += " "
        lines.append(line)

    # X 轴
    lines.append("      └" + "─" * (len(values) * 2 - 1))
    lines.append("       " + " ".join([f"{l:2}" for l in range(len(labels))]))
    lines.append("       " + " ".join([f"{l[:2]:2}" for l in labels]))

    return "\n".join(lines)

def ascii_risk_matrix(risks: list) -> str:
    """生成 ASCII 风险矩阵"""
    lines = ["\n风险矩阵（影响 vs 概率）\n"]
    lines.append("        低影响          │          高影响")
    lines.append("    ┌─────────────────┼─────────────────┐")
    lines.append("高  │                 │                 │")
    lines.append("概  │   监控          │   优先处置      │")
    lines.append("率  │                 │                 │")
    lines.append("    ├─────────────────┼─────────────────┤")
    lines.append("低  │                 │                 │")
    lines.append("概  │   接受/记录     │   缓解后观察    │")
    lines.append("率  │                 │                 │")
    lines.append("    └─────────────────┴─────────────────┘\n")

    # 标记风险位置
    for risk in risks:
        name = risk.get('name', '')
        level = risk.get('level', 'medium')
        symbol = '⚠' if level == 'high' else '⚡' if level == 'medium' else '✓'
        lines.append(f"  {symbol} {name} ({level})")

    return "\n".join(lines)

def generate_markdown(data: dict) -> str:
    """生成完整 Markdown 报告"""
    meta = data.get('metadata', {})
    exec_summary = data.get('executive_summary', {})
    research_scope = data.get('research_scope', {})
    solutions = data.get('solutions', [])
    comparison = data.get('comparison_matrix', {})
    roi = data.get('roi_analysis', {})
    risks = data.get('risks', [])
    confidence = data.get('confidence', {})
    actions = data.get('next_actions', [])

    md = f"""# {meta.get('title', 'DeepSee 技术调研报告')}

**{meta.get('subtitle', '')}**

- 日期：{meta.get('date', datetime.now().strftime('%Y-%m-%d'))}
- 作者：{meta.get('author', 'DeepSee AI Research')}

---

## 1. 执行摘要

### 核心结论

{exec_summary.get('conclusion', '')}

### 推荐方案

"""

    for rec in exec_summary.get('recommendations', []):
        md += f"- **{rec}**\n"

    md += "\n### 关键风险\n\n"
    for risk in exec_summary.get('key_risks', []):
        md += f"- {risk}\n"

    # 调研范围
    md += f"\n---\n\n## 2. 调研范围与数据源\n\n"
    md += f"**复杂度**：{research_scope.get('complexity', 'Medium')} | "
    md += f"**数据源总数**：{len(research_scope.get('sources', []))}\n\n"

    md += "| 来源名称 | 类别 | 质量评分 |\n"
    md += "|---------|------|----------|\n"
    for src in research_scope.get('sources', []):
        md += f"| {src.get('name', '')} | {src.get('category', '')} | {src.get('score', 0)}/10 |\n"

    # 技术方案
    md += f"\n---\n\n## 3. 技术选型方案\n\n"
    for i, sol in enumerate(solutions, 1):
        md += f"### 方案 {i}：{sol.get('name', '')}\n\n"
        md += f"{sol.get('description', '')}\n\n"
        md += "**优势**\n"
        for pro in sol.get('pros', []):
            md += f"- ✓ {pro}\n"
        md += "\n**劣势**\n"
        for con in sol.get('cons', []):
            md += f"- ✗ {con}\n\n"

    # 竞品对标
    md += f"---\n\n## 4. 竞品对标分析\n\n"

    if comparison.get('matrix'):
        md += "| 方案 | " + " | ".join(comparison.get('dimensions', [])) + " | 综合评分 |\n"
        md += "|------|" + "|".join(["---"] * (len(comparison.get('dimensions', [])) + 1)) + "|\n"
        for row in comparison.get('matrix', []):
            scores = " | ".join([str(s) for s in row.get('scores', [])])
            md += f"| {row.get('name', '')} | {scores} | **{row.get('total_score', 0)}** |\n"

    # ASCII 热力图
    if comparison.get('heatmap_data'):
        md += ascii_heatmap(comparison.get('heatmap_data', {}))

    # ROI 分析
    md += f"\n---\n\n## 5. ROI 与商业价值\n\n"

    if roi.get('tco'):
        md += "### 总体拥有成本 (TCO)\n\n"
        tco_data = {
            'title': 'TCO 对比（万元）',
            'categories': list(roi.get('tco', {}).keys()),
            'values': [sum(v.values()) if isinstance(v, dict) else v for v in roi.get('tco', {}).values()]
        }
        md += ascii_bar_chart(tco_data)

    if roi.get('payback_period'):
        md += f"\n\n**回本周期**：{roi.get('payback_period', '')}\n"

    # 风险评估
    md += f"\n---\n\n## 6. 风险评估\n\n"
    md += ascii_risk_matrix(risks)

    md += "\n### 风险详情\n\n"
    for risk in risks:
        level_emoji = '🔴' if risk.get('level') == 'high' else '🟡' if risk.get('level') == 'medium' else '🟢'
        md += f"{level_emoji} **{risk.get('name', '')}** ({risk.get('level', 'medium')})\n\n"
        md += f"{risk.get('description', '')}\n\n"
        if risk.get('mitigation'):
            md += f"*缓解措施*：{risk.get('mitigation', '')}\n\n"

    # 置信度分析
    md += f"---\n\n## 7. 置信度分析\n\n"
    md += f"**整体置信度**：{confidence.get('overall_confidence', 0)}%\n"

    if confidence.get('breakdown'):
        md += "\n### 分项置信度\n\n"
        conf_data = {
            'title': '置信度演变',
            'labels': list(confidence.get('breakdown', {}).keys()),
            'values': list(confidence.get('breakdown', {}).values())
        }
        md += ascii_line_chart(conf_data)

    # 行动建议
    md += f"\n---\n\n## 8. 行动建议\n\n"
    for i, action in enumerate(actions, 1):
        md += f"### {i}. {action.get('title', '')}\n\n"
        md += f"{action.get('description', '')}\n\n"
        if action.get('timeline'):
            md += f"**时间线**：{action.get('timeline', '')}\n\n"

    # 页脚
    md += f"""---

**DeepSee** - 智能技术调研与方案评估系统

© {datetime.now().year} DeepSee AI Research. All rights reserved.
"""

    return md

def main() -> None:
    ap = argparse.ArgumentParser(description="生成 DeepSee Markdown 报告")
    ap.add_argument("-i", "--input", required=True, type=Path, help="JSON 数据文件")
    ap.add_argument("-o", "--output", required=True, type=Path, help="输出 Markdown 文件")
    args = ap.parse_args()

    if not args.input.exists():
        print(f"错误: 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误: JSON 解析失败: {e}", file=sys.stderr)
        sys.exit(1)

    md = generate_markdown(data)
    args.output.write_text(md, encoding="utf-8")
    print(f"✓ Markdown 报告已生成: {args.output.resolve()}")

if __name__ == "__main__":
    main()
