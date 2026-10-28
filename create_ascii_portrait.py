#!/usr/bin/env python3
"""Create an animated ASCII portrait SVG from a local photo (Pillow required)."""
from pathlib import Path
from PIL import Image, ImageOps, ImageEnhance
import argparse, html
p=argparse.ArgumentParser()
p.add_argument('photo',help='local JPG/PNG')
p.add_argument('--output', default='assets/ascii-portrait.svg')
a=p.parse_args()
im=Image.open(a.photo).convert('L')
im=ImageOps.fit(im,(40,31))
im=ImageEnhance.Contrast(im).enhance(1.55)
chars='@#%xo*+=-:. '
rows=[]
for y in range(im.height):
    row=''.join(chars[min(len(chars)-1, int(im.getpixel((x,y))/256*len(chars)))] for x in range(im.width))
    delay=round(y*.09,2)
    rows.append(f'<text x="18" y="{32+y*13}" opacity="0">{html.escape(row)}<animate attributeName="opacity" values="0;0;1;1" keyTimes="0;{delay/7:.3f};{(delay+.08)/7:.3f};1" dur="7s" repeatCount="indefinite"/></text>')
svg=('<svg xmlns="http://www.w3.org/2000/svg" width="410" height="460" viewBox="0 0 410 460">'
'<rect width="410" height="460" rx="16" fill="#151512"/><g fill="#c4a775" font-family="monospace" font-size="12" xml:space="preserve">'
+''.join(rows)+'</g></svg>')
Path(a.output).parent.mkdir(parents=True,exist_ok=True)
Path(a.output).write_text(svg,encoding='utf-8')
print(a.output)
