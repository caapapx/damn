#!/usr/bin/env python3
"""
从 JSON 生成 damn 报告用 PNG 图表。需要 matplotlib: pip install matplotlib
用法: python3 render_damn_charts.py -i damn-charts.json -o ./out
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import matplotlib
    import numpy as np
except ImportError:
    print("需要安装 matplotlib 和 numpy: pip install matplotlib numpy", file=sys.stderr)
    sys.exit(1)

matplotlib.use("Agg")


def _ensure_out(d: Path) -> None:
    d.mkdir(parents=True, exist_ok=True)


def heatmap(data: dict, out: Path) -> None:
    rows, cols = data["rows"], data["cols"]
    values = np.array(data["values"], dtype=float)
    fig, ax = plt.subplots(figsize=(max(6, len(cols) * 1.2), max(4, len(rows) * 0.6)))
    im = ax.imshow(values, cmap="YlOrRd", aspect="auto", vmin=0, vmax=10)
    ax.set_xticks(range(len(cols)), labels=cols, rotation=35, ha="right")
    ax.set_yticks(range(len(rows)), labels=rows)
    for i in range(len(rows)):
        for j in range(len(cols)):
            ax.text(j, i, f"{values[i, j]:.1f}", ha="center", va="center", color="black", fontsize=9)
    ax.set_title(data.get("title", "heatmap"))
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(out / "heatmap.png", dpi=150)
    plt.close(fig)


def radar(data: dict, out: Path) -> None:
    alts = data["alternatives"]
    axes_labels = data["axes"]
    scores = np.array(data["scores"], dtype=float)
    n = len(axes_labels)
    theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
    theta_close = np.concatenate([theta, theta[:1]])
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    for idx, name in enumerate(alts):
        vals = np.concatenate([scores[idx], scores[idx, :1]])
        ax.plot(theta_close, vals, "o-", linewidth=1.5, label=name)
        ax.fill(theta_close, vals, alpha=0.12)
    ax.set_thetagrids(np.degrees(theta), axes_labels)
    ax.set_ylim(0, 10)
    ax.set_title(data.get("title", "radar"), y=1.08)
    ax.legend(loc="upper right", bbox_to_anchor=(1.28, 1.1))
    fig.tight_layout()
    fig.savefig(out / "radar.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def grouped_bar(data: dict, out: Path) -> None:
    cats = data["categories"]
    series: dict = data["series"]
    names = list(series.keys())
    x = np.arange(len(cats))
    w = 0.8 / max(len(names), 1)
    fig, ax = plt.subplots(figsize=(max(7, len(cats) * 1.3), 5))
    for i, sname in enumerate(names):
        offset = (i - len(names) / 2 + 0.5) * w
        ax.bar(x + offset, series[sname], width=w * 0.9, label=sname)
    ax.set_xticks(x, labels=cats, rotation=25, ha="right")
    ax.set_title(data.get("title", "grouped_bar"))
    ax.legend()
    ax.set_ylabel("数值")
    fig.tight_layout()
    fig.savefig(out / "grouped_bar.png", dpi=150)
    plt.close(fig)


def source_bars(data: dict, out: Path) -> None:
    srcs = data["sources"]
    names = [s["name"] for s in srcs]
    scores = [float(s["score"]) for s in srcs]
    fig, ax = plt.subplots(figsize=(7, max(3, len(names) * 0.45)))
    y = range(len(names))
    ax.barh(y, scores, color="steelblue")
    ax.set_yticks(list(y), labels=names)
    ax.set_xlim(0, 10)
    ax.set_xlabel("质量分 (0–10)")
    ax.set_title(data.get("title", "source_bars"))
    fig.tight_layout()
    fig.savefig(out / "source_bars.png", dpi=150)
    plt.close(fig)


def tornado(data: dict, out: Path) -> None:
    baseline = float(data["baseline"])
    variables = data["variables"]
    names = [v["name"] for v in variables]
    lows = [baseline * float(v["low"]) for v in variables]
    highs = [baseline * float(v["high"]) for v in variables]
    spread = [max(abs(h - baseline), abs(l - baseline)) for h, l in zip(highs, lows)]
    order = sorted(range(len(names)), key=lambda i: spread[i], reverse=True)
    names_o = [names[i] for i in order]
    lows_o = [lows[i] for i in order]
    highs_o = [highs[i] for i in order]
    fig, ax = plt.subplots(figsize=(8, max(4, len(names) * 0.5)))
    y = np.arange(len(names_o))
    for i, yi in enumerate(y):
        lo, hi = sorted([lows_o[i], highs_o[i]])
        ax.barh(yi, hi - lo, left=lo, height=0.65, color="coral", alpha=0.85)
    ax.axvline(baseline, color="black", linestyle="--", linewidth=1, label=f"baseline={baseline}")
    ax.set_yticks(y, labels=names_o)
    ax.set_title(data.get("title", "tornado"))
    ax.legend()
    fig.tight_layout()
    fig.savefig(out / "tornado.png", dpi=150)
    plt.close(fig)


def confidence_line(data: dict, out: Path) -> None:
    labels = data["labels"]
    values = [float(v) for v in data["values"]]
    fig, ax = plt.subplots(figsize=(max(6, len(labels) * 1.0), 4))
    ax.plot(labels, values, "o-", linewidth=2, markersize=8, color="darkgreen")
    ax.set_ylim(0, 100)
    ax.set_ylabel("置信度 %")
    ax.set_title(data.get("title", "confidence"))
    ax.tick_params(axis="x", rotation=25)
    fig.tight_layout()
    fig.savefig(out / "confidence_line.png", dpi=150)
    plt.close(fig)


HANDLERS = {
    "heatmap": heatmap,
    "radar": radar,
    "grouped_bar": grouped_bar,
    "source_bars": source_bars,
    "tornado": tornado,
    "confidence_line": confidence_line,
}


def main() -> None:
    ap = argparse.ArgumentParser(description="Render damn report charts from JSON")
    ap.add_argument("-i", "--input", required=True, type=Path, help="JSON 配置文件")
    ap.add_argument("-o", "--output", required=True, type=Path, help="PNG 输出目录")
    args = ap.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    _ensure_out(args.output)
    done = []
    for key, fn in HANDLERS.items():
        if key not in payload or payload[key] is None:
            continue
        fn(payload[key], args.output)
        name_map = {
            "heatmap": "heatmap.png",
            "radar": "radar.png",
            "grouped_bar": "grouped_bar.png",
            "source_bars": "source_bars.png",
            "tornado": "tornado.png",
            "confidence_line": "confidence_line.png",
        }
        done.append(name_map.get(key, f"{key}.png"))
    if not done:
        print("JSON 中未包含支持的图表块", file=sys.stderr)
        sys.exit(2)
    print("已生成:", ", ".join(done), "->", args.output.resolve())


if __name__ == "__main__":
    main()
