#!/usr/bin/env python3.13
"""Entrypoint for the news-image-20261120 v2.1 entry.

Standard library only. The front page is rendered at build time by
draw.py and shipped in this repository as entry.png; this script only
carries that finished image into the directory the grader reads.

The split is deliberate: the grading container runs Python with the
standard library alone, so nothing here imports Pillow or any other
third-party package.
"""

import os
import shutil
import sys


def _source_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.png")


def _output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    src = _source_path()
    size = os.path.getsize(src)
    if size < 1 or size > 1048576:
        print("entry.png size out of range: %d bytes" % size, file=sys.stderr)
        return 1
    out_dir = _output_dir()
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    copied = os.path.getsize(dst)
    if copied != size:
        print("copy size mismatch: %d != %d" % (copied, size), file=sys.stderr)
        return 1
    print("copied entry.png (%d bytes) to %s" % (copied, dst))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
