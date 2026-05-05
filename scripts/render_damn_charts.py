#!/usr/bin/env python3
"""Compatibility wrapper for renamed damn chart command."""

from pathlib import Path
import runpy


if __name__ == "__main__":
    candidates = [p for p in Path(__file__).parent.glob("render_*_charts.py") if p.name != Path(__file__).name]
    if not candidates:
        raise SystemExit("No backing chart renderer found")
    target = candidates[0]
    runpy.run_path(str(target), run_name="__main__")
