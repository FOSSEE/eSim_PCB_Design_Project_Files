"""Rasterise an SVG with headless Microsoft Edge (no extra dependencies). Usage: svg2png.py in.svg out.png width_px"""
import os
import re
import subprocess
import sys
import tempfile

from PIL import Image

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"


def main(src, dst, width):
    width = int(width)
    txt = open(src, encoding="utf-8").read()
    m = re.search(r'viewBox="([-0-9.]+) ([-0-9.]+) ([-0-9.]+) ([-0-9.]+)"', txt)
    vw, vh = float(m.group(3)), float(m.group(4))
    height = int(width * vh / vw) + 2
    html = os.path.join(tempfile.gettempdir(), "svg2png_%d.html" % os.getpid())
    uri = "file:///" + os.path.abspath(src).replace("\\", "/")
    open(html, "w").write('<html><body style="margin:0;background:#fff"><img src="%s" style="width:%dpx;display:block"></body></html>'
                          % (uri, width))
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--hide-scrollbars", "--screenshot=" + os.path.abspath(dst),
                    "--window-size=%d,%d" % (width, height), "file:///" + html.replace("\\", "/")],
                   capture_output=True, timeout=240)
    im = Image.open(dst).convert("RGB")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    from PIL import ImageChops
    bbox = ImageChops.difference(im, bg).getbbox()
    if bbox:
        pad = 12
        im = im.crop((max(bbox[0] - pad, 0), max(bbox[1] - pad, 0), min(bbox[2] + pad, im.size[0]), min(bbox[3] + pad, im.size[1])))
    im.save(dst)
    print("png", dst, im.size)


if __name__ == "__main__":
    main(*sys.argv[1:4])
