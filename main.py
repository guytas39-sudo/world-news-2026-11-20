#!/usr/bin/env python3
"""Entry program for news-image-20261120: place the entry image in the output dir.

The image is pre-drawn by draw_image.py at build time. This program copies it
to $MAKEFUN_OUTPUT_DIR/entry.png (falling back to /output/entry.png), so both
runs write identical bytes. Standard library only.
"""
import os
import shutil

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
os.makedirs(out_dir, exist_ok=True)
here = os.path.dirname(os.path.abspath(__file__))
dest = os.path.join(out_dir, "entry.png")
shutil.copyfile(os.path.join(here, "entry.png"), dest)
print("wrote", dest)
