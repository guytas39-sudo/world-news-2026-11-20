#!/usr/bin/env python3
"""Entry program for news-image-20261120: copy the entry image to the output dir.

The image is pre-drawn by draw_image.py (run at build time); this program just
places it at $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png), so both
runs write identical bytes.
"""
import os
import shutil

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
os.makedirs(out_dir, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
shutil.copyfile(os.path.join(here, "entry.png"),
                os.path.join(out_dir, "entry.png"))
print("wrote", os.path.join(out_dir, "entry.png"))
