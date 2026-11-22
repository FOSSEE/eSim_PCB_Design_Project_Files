"""Combine the four copper-layer plots into one labelled 2x2 sheet."""
import os
import sys

from PIL import Image, ImageDraw, ImageFont


def main(d, out):
    names = [("F.Cu", "F.Cu: top signal + GND pour"), ("In1.Cu", "In1.Cu: GND plane"),
             ("In2.Cu", "In2.Cu: +3V3 plane"), ("B.Cu", "B.Cu: bottom signal + GND pour (viewed from top)")]
    ims = [Image.open(os.path.join(d, "layer_%s.png" % n)).convert("RGB") for n, _ in names]
    w = max(i.size[0] for i in ims)
    h = max(i.size[1] for i in ims)
    lab = 46
    sheet = Image.new("RGB", (2 * w + 30, 2 * (h + lab) + 30), "white")
    dr = ImageDraw.Draw(sheet)
    try:
        f = ImageFont.truetype("arialbd.ttf", 30)
    except OSError:
        f = ImageFont.load_default()
    for k, (im, (_, t)) in enumerate(zip(ims, names)):
        x = (k % 2) * (w + 30)
        y = (k // 2) * (h + lab + 30)
        dr.text((x + 8, y + 6), t, fill=(20, 50, 100), font=f)
        sheet.paste(im, (x, y + lab))
    sheet.save(out)
    print("sheet", out, sheet.size)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
