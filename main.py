#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261120 entry.

Renders the front page (see draw.py) into the output directory the
grader names in MAKEFUN_OUTPUT_DIR, defaulting to ./out.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import draw  # noqa: E402


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", os.path.join(HERE, "out"))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    draw.render(out_path)
    print("wrote", out_path, os.path.getsize(out_path), "bytes")


if __name__ == "__main__":
    main()
