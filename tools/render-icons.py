#!/usr/bin/env python3
"""VPN Master — آیکون‌ساز

آیکون «سپر + تیک» را در همهٔ اندازه‌های لازم برای اندروید می‌سازد.
اجرا:  python3 tools/render-icons.py
"""
from PIL import Image, ImageDraw
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(ROOT, "app/src/main/res")

S = 1024
BG1, BG2 = (13, 17, 25), (21, 30, 45)      # پس‌زمینهٔ تیره
G1, G2 = (54, 232, 172), (22, 150, 124)    # سبز سپر
INK = (8, 32, 26, 255)                     # رنگ تیک


def shield_mask(w, h, cx, cy):
    m = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(m)
    x0, x1 = cx - w / 2, cx + w / 2
    top, bot = cy - h / 2, cy + h / 2
    body = h * 0.66
    d.rounded_rectangle([x0, top, x1, top + body], radius=w * 0.13, fill=255)
    d.polygon([(x0, top + body - h * 0.06), (x1, top + body - h * 0.06), (cx, bot)], fill=255)
    return m


def gradient():
    g = Image.new("RGBA", (S, S))
    d = ImageDraw.Draw(g)
    for y in range(S):
        t = y / S
        d.line([(0, y), (S, y)], fill=tuple(int(G1[i] + (G2[i] - G1[i]) * t) for i in range(3)) + (255,))
    return g


def icon(size, rounded=False, with_bg=True):
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if with_bg:
        for y in range(S):
            t = y / S
            d.line([(0, y), (S, y)],
                   fill=tuple(int(BG1[i] + (BG2[i] - BG1[i]) * t) for i in range(3)) + (255,))
        if rounded:
            mask = Image.new("L", (S, S), 0)
            ImageDraw.Draw(mask).ellipse([0, 0, S - 1, S - 1], fill=255)
            im.putalpha(mask)
    pad = S * (0.20 if rounded else 0.17)
    w = h = S - 2 * pad
    im.paste(gradient(), (0, 0), shield_mask(w, h, S / 2, S / 2))
    d2 = ImageDraw.Draw(im)
    lw = int(S * 0.068)
    chk = [(S * 0.375, S * 0.505), (S * 0.468, S * 0.60), (S * 0.635, S * 0.415)]
    d2.line(chk, fill=INK, width=lw, joint="curve")
    for p in chk:
        r = lw / 2 * 0.98
        d2.ellipse([p[0] - r, p[1] - r, p[0] + r, p[1] + r], fill=INK)
    return im.resize((size, size), Image.LANCZOS)


SIZES = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}

for dpi, px in SIZES.items():
    folder = os.path.join(RES, f"mipmap-{dpi}")
    os.makedirs(folder, exist_ok=True)
    icon(px).save(os.path.join(folder, "ic_launcher.png"))
    icon(px, rounded=True).save(os.path.join(folder, "ic_launcher_round.png"))

os.makedirs("icons", exist_ok=True)
icon(512).save("icons/preview_512.png")
icon(512, rounded=True).save("icons/preview_round_512.png")
print("✔ آیکون‌ها ساخته شدند در", RES)
