"""Grading entrypoint for the news-image-20261120 entry.

Standard library only. The grading container installs nothing, so this
file copies the pre-rendered entry.png into the output directory and
verifies the copy byte for byte. It never imports the renderer.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        sys.stderr.write("entry.png copy size mismatch\n")
        return 1
    with open(src, "rb") as f_src, open(dst, "rb") as f_dst:
        if f_src.read() != f_dst.read():
            sys.stderr.write("entry.png copy content mismatch\n")
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
