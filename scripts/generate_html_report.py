#!/usr/bin/env python3
"""
DeepSee HTML 报告生成器 - 专业分析机构风格
用法: python3 generate_html_report.py -i report_data.json -o report.html
"""
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

def generate_html(data: dict) -> str:
    """生成完整 HTML 报告"""

    # 提取数据
    meta = data.get("metadata", {})
    exec_summary = data.get("executive_summary", {})
    research_scope = data.get("research_scope", {})
    solutions = data.get("solutions", [])
    comparison = data.get("comparison_matrix", {})
    roi = data.get("roi_analysis", {})
    risks = data.get("risks", [])
    confidence = data.get("confidence", {})
    actions = data.get("next_actions", [])
    charts = data.get("charts", {})

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{meta.get('title', 'DeepSee 技术调研报告')}</title>
    <style>
        {get_styles()}
    </style>
</head>
<body>
    <div class="report-container">
        {generate_cover(meta)}
        {generate_toc()}
        {generate_exec_summary(exec_summary)}
        {generate_research_scope(research_scope)}
        {generate_solutions(solutions)}
        {generate_comparison(comparison, charts)}
        {generate_roi(roi, charts)}
        {generate_risks(risks)}
        {generate_confidence(confidence, charts)}
        {generate_actions(actions)}
        {generate_footer(meta)}
    </div>
    <script>
        {get_scripts()}
    </script>
</body>
</html>"""

    return html

def get_styles() -> str:
    """专业分析机构风格样式"""
    return """
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC',
                         'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
            line-height: 1.6;
            color: #1a1a1a;
            background: #f8f9fa;
        }

        .report-container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 40px rgba(0,0,0,0.08);
        }

        /* 封面 */
        .cover {
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 60px;
            position: relative;
            overflow: hidden;
        }

        .cover::before {
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: grid-move 20s linear infinite;
        }

        @keyframes grid-move {
            0% { transform: translate(0, 0); }
            100% { transform: translate(50px, 50px); }
        }

        .cover-content { position: relative; z-index: 1; }
        .cover h1 { font-size: 3.5em; font-weight: 700; margin-bottom: 20px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
        .cover .subtitle { font-size: 1.4em; opacity: 0.95; margin-bottom: 40px; }
        .cover .meta { font-size: 1.1em; opacity: 0.9; }

        /* 目录 */
        .toc {
            padding: 80px 60px;
            background: #fafbfc;
            border-bottom: 3px solid #667eea;
        }

        .toc h2 { font-size: 2em; margin-bottom: 30px; color: #667eea; }
        .toc-list { list-style: none; }
        .toc-item {
            padding: 15px 20px;
            margin: 10px 0;
            background: white;
            border-left: 4px solid #667eea;
            cursor: pointer;
            transition: all 0.3s;
            border-radius: 4px;
        }
        .toc-item:hover {
            transform: translateX(10px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }
        .toc-item a {
            text-decoration: none;
            color: #1a1a1a;
            font-size: 1.1em;
            display: flex;
            justify-content: space-between;
        }

        /* 章节 */
        .section {
            padding: 80px 60px;
            border-bottom: 1px solid #e1e4e8;
        }

        .section-header {
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 3px solid #667eea;
        }

        .section-number {
            display: inline-block;
            width: 50px;
            height: 50px;
            line-height: 50px;
            text-align: center;
            background: #667eea;
            color: white;
            border-radius: 50%;
            font-weight: bold;
            margin-right: 15px;
            font-size: 1.2em;
        }

        .section h2 {
            display: inline-block;
            font-size: 2.2em;
            color: #1a1a1a;
            vertical-align: middle;
        }

        /* 执行摘要 */
        .exec-summary {
            background: linear-gradient(to right, #f8f9fa, #ffffff);
        }

        .key-findings {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }

        .finding-card {
            padding: 25px;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            transition: transform 0.3s;
        }

        .finding-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 16px rgba(0,0,0,0.12);
        }

        .finding-card h4 {
            color: #667eea;
            margin-bottom: 12px;
            font-size: 1.2em;
        }

        /* 表格 */
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
            background: white;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border-radius: 8px;
            overflow: hidden;
        }

        .data-table thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .data-table th {
            padding: 18px 15px;
            text-align: left;
            font-weight: 600;
            font-size: 1.05em;
        }

        .data-table td {
            padding: 15px;
            border-bottom: 1px solid #e1e4e8;
        }

        .data-table tbody tr:hover {
            background: #f8f9fa;
        }

        .score-cell {
            font-weight: bold;
            text-align: center;
        }

        .score-high { color: #28a745; }
        .score-medium { color: #ffc107; }
        .score-low { color: #dc3545; }

        /* 图表容器 */
        .chart-container {
            margin: 40px 0;
            padding: 30px;
            background: #fafbfc;
            border-radius: 8px;
            border: 1px solid #e1e4e8;
        }

        .chart-title {
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 20px;
            color: #1a1a1a;
        }

        .chart-canvas {
            width: 100%;
            height: 400px;
        }

        /* 风险卡片 */
        .risk-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }

        .risk-card {
            padding: 20px;
            border-radius: 8px;
            border: 2px solid;
            background: white;
        }

        .risk-high { border-color: #dc3545; background: #fff5f5; }
        .risk-medium { border-color: #ffc107; background: #fffbf0; }
        .risk-low { border-color: #28a745; background: #f0fff4; }

        .risk-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .risk-badge {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            color: white;
        }

        .badge-high { background: #dc3545; }
        .badge-medium { background: #ffc107; color: #1a1a1a; }
        .badge-low { background: #28a745; }

        /* 置信度指示器 */
        .confidence-bar {
            height: 40px;
            background: #e1e4e8;
            border-radius: 20px;
            overflow: hidden;
            position: relative;
            margin: 20px 0;
        }

        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #28a745, #667eea);
            transition: width 1s ease-out;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 15px;
            color: white;
            font-weight: bold;
        }

        /* 行动项 */
        .action-list {
            list-style: none;
            counter-reset: action-counter;
        }

        .action-item {
            counter-increment: action-counter;
            padding: 20px;
            margin: 15px 0;
            background: white;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            position: relative;
            padding-left: 70px;
        }

        .action-item::before {
            content: counter(action-counter);
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            width: 35px;
            height: 35px;
            line-height: 35px;
            text-align: center;
            background: #667eea;
            color: white;
            border-radius: 50%;
            font-weight: bold;
        }

        /* 页脚 */
        .footer {
            padding: 40px 60px;
            background: #1a1a1a;
            color: #999;
            text-align: center;
        }

        .footer-logo {
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 15px;
        }

        /* 响应式 */
        @media (max-width: 768px) {
            .section { padding: 40px 30px; }
            .cover h1 { font-size: 2em; }
            .section h2 { font-size: 1.6em; }
            .key-findings, .risk-grid { grid-template-columns: 1fr; }
        }

        /* 打印样式 */
        @media print {
            .cover { page-break-after: always; }
            .section { page-break-inside: avoid; }
            .toc-item:hover { transform: none; }
        }
    """

def generate_cover(meta: dict) -> str:
    """生成封面"""
    title = meta.get('title', 'DeepSee 技术调研报告')
    subtitle = meta.get('subtitle', '智能技术选型与方案评估')
    date = meta.get('date', datetime.now().strftime('%Y年%m月%d日'))
    author = meta.get('author', 'DeepSee AI Research')

    return f"""
    <div class="cover">
        <div class="cover-content">
            <h1>{title}</h1>
            <div class="subtitle">{subtitle}</div>
            <div class="meta">
                <div>{date}</div>
                <div style="margin-top: 10px;">{author}</div>
            </div>
        </div>
    </div>
    """

def generate_toc() -> str:
    """生成目录"""
    sections = [
        ("1", "执行摘要", "exec-summary"),
        ("2", "调研范围与数据源", "research-scope"),
        ("3", "技术选型方案", "solutions"),
        ("4", "竞品对标分析", "comparison"),
        ("5", "ROI与商业价值", "roi"),
        ("6", "风险评估", "risks"),
        ("7", "置信度分析", "confidence"),
        ("8", "行动建议", "actions"),
    ]

    items = ""
    for num, title, anchor in sections:
        items += f"""
        <li class="toc-item">
            <a href="#{anchor}">
                <span>{num}. {title}</span>
                <span>→</span>
            </a>
        </li>
        """

    return f"""
    <div class="toc">
        <h2>目录</h2>
        <ul class="toc-list">{items}</ul>
    </div>
    """

def generate_exec_summary(data: dict) -> str:
    """生成执行摘要"""
    conclusion = data.get('conclusion', '暂无结论')
    recommendations = data.get('recommendations', [])
    key_risks = data.get('key_risks', [])

    findings_html = ""
    if recommendations:
        findings_html += f"""
        <div class="finding-card">
            <h4>推荐方案</h4>
            <p>{' | '.join(recommendations)}</p>
        </div>
        """

    if key_risks:
        findings_html += f"""
        <div class="finding-card">
            <h4>关键风险</h4>
            <p>{' | '.join(key_risks)}</p>
        </div>
        """

    return f"""
    <div id="exec-summary" class="section exec-summary">
        <div class="section-header">
            <span class="section-number">1</span>
            <h2>执行摘要</h2>
        </div>
        <div style="font-size: 1.15em; line-height: 1.8; margin-bottom: 30px;">
            {conclusion}
        </div>
        <div class="key-findings">{findings_html}</div>
    </div>
    """

def generate_research_scope(data: dict) -> str:
    """生成调研范围"""
    sources = data.get('sources', [])
    complexity = data.get('complexity', 'Medium')
    total_sources = len(sources)

    sources_html = ""
    for src in sources:
        name = src.get('name', '')
        category = src.get('category', '')
        score = src.get('score', 0)
        score_class = 'score-high' if score >= 8 else 'score-medium' if score >= 6 else 'score-low'

        sources_html += f"""
        <tr>
            <td>{name}</td>
            <td>{category}</td>
            <td class="score-cell {score_class}">{score}/10</td>
        </tr>
        """

    return f"""
    <div id="research-scope" class="section">
        <div class="section-header">
            <span class="section-number">2</span>
            <h2>调研范围与数据源</h2>
        </div>
        <p style="font-size: 1.1em; margin-bottom: 20px;">
            复杂度: <strong>{complexity}</strong> | 数据源总数: <strong>{total_sources}</strong>
        </p>
        <table class="data-table">
            <thead>
                <tr>
                    <th>来源名称</th>
                    <th>类别</th>
                    <th>质量评分</th>
                </tr>
            </thead>
            <tbody>{sources_html}</tbody>
        </table>
    </div>
    """

def generate_solutions(solutions: list) -> str:
    """生成技术方案"""
    solutions_html = ""

    for idx, sol in enumerate(solutions, 1):
        name = sol.get('name', f'方案{idx}')
        description = sol.get('description', '')
        pros = sol.get('pros', [])
        cons = sol.get('cons', [])

        pros_html = "".join([f"<li>✓ {p}</li>" for p in pros])
        cons_html = "".join([f"<li>✗ {c}</li>" for c in cons])

        solutions_html += f"""
        <div class="finding-card" style="margin: 20px 0;">
            <h3 style="color: #667eea; margin-bottom: 15px;">方案 {idx}: {name}</h3>
            <p style="margin-bottom: 15px;">{description}</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4 style="color: #28a745; margin-bottom: 10px;">优势</h4>
                    <ul style="list-style: none; padding-left: 0;">{pros_html}</ul>
                </div>
                <div>
                    <h4 style="color: #dc3545; margin-bottom: 10px;">劣势</h4>
                    <ul style="list-style: none; padding-left: 0;">{cons_html}</ul>
                </div>
            </div>
        </div>
        """

    return f"""
    <div id="solutions" class="section">
        <div class="section-header">
            <span class="section-number">3</span>
            <h2>技术选型方案</h2>
        </div>
        {solutions_html}
    </div>
    """

def generate_comparison(data: dict, charts: dict) -> str:
    """生成竞品对标矩阵"""
    matrix = data.get('matrix', [])
    dimensions = data.get('dimensions', [])
    if not matrix or not dimensions:
        return ""
    header_html = "<th>方案</th>" + "".join([f"<th>{d}</th>" for d in dimensions]) + "<th>综合评分</th>"
    rows_html = ""
    for row in matrix:
        name = row.get('name', '')
        scores = row.get('scores', [])
        total = row.get('total_score', 0)
        score_cells = ""
        for score in scores:
            sc = 'score-high' if score >= 8 else 'score-medium' if score >= 6 else 'score-low'
            score_cells += f'<td class="score-cell {sc}">{score}</td>'
        tc = 'score-high' if total >= 8 else 'score-medium' if total >= 6 else 'score-low'
        rows_html += f'<tr><td><strong>{name}</strong></td>{score_cells}<td class="score-cell {tc}"><strong>{total}</strong></td></tr>'
    chart_html = '<div class="chart-container"><div class="chart-title">方案对比雷达图</div><canvas id="radarChart" class="chart-canvas"></canvas></div>' if charts.get('radar_chart') else ''
    return f'<div id="comparison" class="section"><div class="section-header"><span class="section-number">4</span><h2>竞品对标分析</h2></div><table class="data-table"><thead><tr>{header_html}</tr></thead><tbody>{rows_html}</tbody></table>{chart_html}</div>'

def generate_roi(data: dict, charts: dict) -> str:
    """生成ROI分析"""
    tco = data.get('tco', {})
    payback = data.get('payback_period', '')
    tco_html = ""
    if tco:
        for solution, costs in tco.items():
            total = sum(costs.values()) if isinstance(costs, dict) else 0
            tco_html += f'<div class="finding-card"><h4>{solution}</h4><p style="font-size: 1.5em; font-weight: bold; color: #667eea;">¥{total:,.0f}</p></div>'
    chart_html = '<div class="chart-container"><div class="chart-title">TCO 成本对比</div><canvas id="tcoChart" class="chart-canvas"></canvas></div>' if charts.get('tco_chart') else ''
    payback_html = f'<p style="font-size: 1.1em; margin: 20px 0;"><strong>回本周期:</strong> {payback}</p>' if payback else ''
    return f'<div id="roi" class="section"><div class="section-header"><span class="section-number">5</span><h2>ROI与商业价值</h2></div><div class="key-findings">{tco_html}</div>{payback_html}{chart_html}</div>'

def generate_risks(risks: list) -> str:
    """生成风险评估"""
    risk_cards = ""
    level_map = {'high': ('高风险', 'risk-high', 'badge-high'), 'medium': ('中风险', 'risk-medium', 'badge-medium'), 'low': ('低风险', 'risk-low', 'badge-low')}
    for risk in risks:
        name = risk.get('name', '')
        level = risk.get('level', 'medium')
        desc = risk.get('description', '')
        mit = risk.get('mitigation', '')
        lt, cc, bc = level_map.get(level, level_map['medium'])
        mit_html = f'<p style="font-size: 0.95em; color: #666;"><strong>缓解:</strong> {mit}</p>' if mit else ''
        risk_cards += f'<div class="risk-card {cc}"><div class="risk-header"><h4>{name}</h4><span class="risk-badge {bc}">{lt}</span></div><p style="margin-bottom: 10px;">{desc}</p>{mit_html}</div>'
    return f'<div id="risks" class="section"><div class="section-header"><span class="section-number">6</span><h2>风险评估</h2></div><div class="risk-grid">{risk_cards}</div></div>'

def generate_confidence(data: dict, charts: dict) -> str:
    """生成置信度分析"""
    overall = data.get('overall_confidence', 0)
    breakdown = data.get('breakdown', {})
    breakdown_html = ""
    for item, conf in breakdown.items():
        breakdown_html += f'<div style="margin: 15px 0;"><div style="display: flex; justify-content: space-between; margin-bottom: 5px;"><span>{item}</span><span><strong>{conf}%</strong></span></div><div class="confidence-bar" style="height: 20px;"><div class="confidence-fill" style="width: {conf}%;"></div></div></div>'
    bd_section = f'<div><h3 style="margin: 30px 0 15px 0;">分项置信度</h3>{breakdown_html}</div>' if breakdown else ''
    return f'<div id="confidence" class="section"><div class="section-header"><span class="section-number">7</span><h2>置信度分析</h2></div><div style="margin: 30px 0;"><h3 style="margin-bottom: 15px;">整体置信度</h3><div class="confidence-bar"><div class="confidence-fill" style="width: {overall}%;">{overall}%</div></div></div>{bd_section}</div>'

def generate_actions(actions: list) -> str:
    """生成行动建议"""
    action_items = ""
    for action in actions:
        title = action.get('title', '')
        desc = action.get('description', '')
        timeline = action.get('timeline', '')
        tl_html = f'<p style="margin-top: 8px; color: #667eea; font-weight: 600;">时间线: {timeline}</p>' if timeline else ''
        action_items += f'<li class="action-item"><h4 style="margin-bottom: 8px;">{title}</h4><p>{desc}</p>{tl_html}</li>'
    return f'<div id="actions" class="section"><div class="section-header"><span class="section-number">8</span><h2>行动建议</h2></div><ul class="action-list">{action_items}</ul></div>'

def generate_footer(meta: dict) -> str:
    """生成页脚"""
    return f'<div class="footer"><div class="footer-logo">DeepSee</div><p>智能技术调研与方案评估系统</p><p style="margin-top: 10px; font-size: 0.9em;">© {datetime.now().year} DeepSee AI Research. All rights reserved.</p></div>'

def get_scripts() -> str:
    """JavaScript 交互和图表"""
    return """
        // 平滑滚动
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });

        // 置信度条动画
        window.addEventListener('load', () => {
            const fills = document.querySelectorAll('.confidence-fill');
            fills.forEach(fill => {
                const width = fill.style.width;
                fill.style.width = '0%';
                setTimeout(() => { fill.style.width = width; }, 100);
            });
        });

        // Chart.js 图表渲染（如果有数据）
        function renderCharts(chartData) {
            if (!chartData || !window.Chart) return;

            // 雷达图
            if (chartData.radar && document.getElementById('radarChart')) {
                const ctx = document.getElementById('radarChart').getContext('2d');
                new Chart(ctx, {
                    type: 'radar',
                    data: chartData.radar,
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: { r: { beginAtZero: true, max: 10 } }
                    }
                });
            }

            // TCO 柱状图
            if (chartData.tco && document.getElementById('tcoChart')) {
                const ctx = document.getElementById('tcoChart').getContext('2d');
                new Chart(ctx, {
                    type: 'bar',
                    data: chartData.tco,
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: { y: { beginAtZero: true } }
                    }
                });
            }
        }

        // 如果页面包含图表数据，渲染它们
        if (typeof chartData !== 'undefined') {
            renderCharts(chartData);
        }
    """

def main() -> None:
    ap = argparse.ArgumentParser(description="生成 DeepSee HTML 报告")
    ap.add_argument("-i", "--input", required=True, type=Path, help="JSON 数据文件")
    ap.add_argument("-o", "--output", required=True, type=Path, help="输出 HTML 文件")
    args = ap.parse_args()

    if not args.input.exists():
        print(f"错误: 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"错误: JSON 解析失败: {e}", file=sys.stderr)
        sys.exit(1)

    html = generate_html(data)
    args.output.write_text(html, encoding="utf-8")
    print(f"✓ HTML 报告已生成: {args.output.resolve()}")

if __name__ == "__main__":
    main()
