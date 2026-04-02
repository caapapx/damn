# DeepSee HTML 报告生成指南

## 快速开始

### 1. 生成报告

```bash
python3 scripts/generate_html_report.py -i report_data.json -o report.html
```

### 2. JSON 数据结构

参考 `references/report-data.example.json`，必需字段：

```json
{
  "metadata": {
    "title": "报告标题",
    "subtitle": "副标题",
    "date": "2026-04-02",
    "author": "作者"
  },
  "executive_summary": {
    "conclusion": "核心结论",
    "recommendations": ["推荐1", "推荐2"],
    "key_risks": ["风险1", "风险2"]
  },
  "solutions": [
    {
      "name": "方案名称",
      "description": "描述",
      "pros": ["优势1"],
      "cons": ["劣势1"]
    }
  ]
}
```

### 3. 报告特性

- ✓ 专业封面（渐变背景 + 动画网格）
- ✓ 交互式目录（平滑滚动）
- ✓ 响应式布局（支持移动端）
- ✓ 数据可视化（置信度条动画）
- ✓ 打印友好（分页优化）
- ✓ 单文件分享（无外部依赖）

### 4. 在 DeepSee Skill 中使用

完成调研后，skill 会自动：
1. 收集所有数据到 JSON
2. 调用生成器创建 HTML
3. 返回报告路径

用户可直接在浏览器打开查看。

## 风格参考

- 封面：Anthropic 风格渐变 + 动画
- 布局：高盛报告式专业排版
- 配色：紫色主题（#667eea）
- 交互：现代 Web 应用体验
