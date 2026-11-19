#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Thursday 19 November 2026.

A one-page newspaper front page rendered with Pillow: masthead and date
bar, the Trump-Xi-Putin summit in Shenzhen as the lead story (with the
three flags drawn from code), GTA VI's launch, Anthropic's record IPO,
the ICJ's genocide verdict in The Hague, a tanker struck in the Strait
of Hormuz, and a world-news ticker along the bottom.

Evening refresh: every "due today" item is replaced with its outcome —
the summit's four-point declaration, the ICJ's guilty verdict, GTA VI's
launch-day numbers, and ANT's first trades.

Output: entry.png next to this script, 1024x1024, under 1 MiB.
Run: python3 draw_news.py
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

W, H = 1024, 1024
MARGIN = 30
CW = W - 2 * MARGIN  # content width: 964

PAPER = (246, 241, 227)
INK = (22, 22, 22)
RED = (155, 28, 28)
NAVY = (31, 42, 68)
GOLD = (196, 145, 20)
GREEN = (34, 139, 34)
GREY = (120, 115, 100)
DARK = (20, 22, 31)
TICKER_GOLD = (227, 179, 65)
WHITE = (242, 242, 242)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines = []
    for para in text.split("\n"):
        line = ""
        for word in para.split(" "):
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= max_width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def text_block(draw, x, y, text, fnt, max_width, leading, color=INK):
    """Draw wrapped text; returns the y coordinate below the last line."""
    for ln in wrap(draw, text, fnt, max_width):
        draw.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y


def star_points(cx, cy, r_outer, r_inner, rotation=-90):
    """Five-pointed star polygon, points alternating outer/inner radius."""
    pts = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        ang = math.radians(rotation + i * 36)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def flag_usa(draw, x, y, w, h):
    stripe = h / 13.0
    for i in range(13):
        c = (178, 34, 52) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe + 1], fill=c)
    cw, ch = w * 0.4, stripe * 7
    draw.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for row in range(5):
        for col in range(6):
            sx = x + cw * (col + 0.5) / 6
            sy = y + ch * (row + 0.5) / 5
            draw.ellipse([sx - 1.6, sy - 1.6, sx + 1.6, sy + 1.6], fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=(60, 60, 60), width=1)


def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    gold = (255, 222, 0)
    draw.polygon(star_points(x + w * 0.22, y + h * 0.28, w * 0.13, w * 0.052), fill=gold)
    for fx, fy, fr in [(0.45, 0.12, 0.05), (0.55, 0.25, 0.05),
                       (0.55, 0.42, 0.05), (0.44, 0.52, 0.05)]:
        draw.polygon(star_points(x + w * fx, y + h * fy, w * fr, w * fr * 0.4),
                     fill=gold)
    draw.rectangle([x, y, x + w, y + h], outline=(60, 60, 60), width=1)


def flag_russia(draw, x, y, w, h):
    band = h / 3.0
    for i, c in enumerate([(255, 255, 255), (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([x, y + i * band, x + w, y + (i + 1) * band + 1], fill=c)
    draw.rectangle([x, y, x + w, y + h], outline=(60, 60, 60), width=1)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.line([(MARGIN, 18), (W - MARGIN, 18)], fill=INK, width=2)
    mast = font(SERIF_BOLD, 76)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=mast)
    d.text(((W - tw) / 2, 24), title, font=mast, fill=INK)
    d.line([(MARGIN, 108), (W - MARGIN, 108)], fill=INK, width=4)
    date_font = font(SANS_BOLD, 23)
    d.text((MARGIN, 118), "THURSDAY, 19 NOVEMBER 2026", font=date_font, fill=INK)
    right = "ONE DAY · ONE PAGE"
    rw = d.textlength(right, font=date_font)
    d.text((W - MARGIN - rw, 118), right, font=date_font, fill=INK)
    d.line([(MARGIN, 150), (W - MARGIN, 150)], fill=INK, width=1)

    # ---------- lead story: the Shenzhen summit ----------
    kicker = font(SANS_BOLD, 20)
    d.text((MARGIN, 160), "THE SHENZHEN SUMMIT", font=kicker, fill=RED)
    head = font(SERIF_BOLD, 47)
    d.text((MARGIN, 186), "TRUMP, XI AND PUTIN SIGN", font=head, fill=INK)
    d.text((MARGIN, 240), "A 'PEACE DECLARATION'", font=head, fill=INK)

    body = font(SANS, 20)
    lead_text = ("After 90 minutes at Kylin Villa, the first three-way meeting of "
                 "the three largest nuclear powers ended with a four-point "
                 "declaration — UN reform, more oil, ICC limits, nuclear-risk "
                 "talks. No deal on Ukraine or Iran.")
    end_y = text_block(d, MARGIN, 304, lead_text, body, 580, 27)

    fx, fw, fh, gap = 640, 112, 75, 8
    flag_fns = [flag_usa, flag_china, flag_russia]
    labels = ["USA", "CHINA", "RUSSIA"]
    lab_font = font(SANS_BOLD, 17)
    for i, fn in enumerate(flag_fns):
        x0 = fx + i * (fw + gap)
        fn(d, x0, 304, fw, fh)
        lw = d.textlength(labels[i], font=lab_font)
        d.text((x0 + (fw - lw) / 2, 384), labels[i], font=lab_font, fill=INK)

    d.line([(MARGIN, 420), (W - MARGIN, 420)], fill=INK, width=1)

    # ---------- middle row: GTA VI / Anthropic IPO ----------
    col_w = 472
    left_x, right_x = MARGIN, 522
    d.line([(512, 430), (512, 700)], fill=GREY, width=1)

    mid_head = font(SERIF_BOLD, 33)
    mid_body = font(SANS, 20)

    d.text((left_x, 430), "GAMING", font=kicker, fill=RED)
    d.text((left_x, 456), "GTA VI LAUNCHES", font=mid_head, fill=INK)
    d.text((left_x, 494), "TODAY", font=mid_head, fill=INK)
    # 99 Metascore badge beside the headline
    bx, by, br = 452, 470, 27
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=GOLD, outline=INK, width=2)
    badge_font = font(SANS_BOLD, 26)
    bw = d.textlength("99", font=badge_font)
    d.text((bx - bw / 2, by - 17), "99", font=badge_font, fill=NAVY)
    gta = ("Launched at midnight local time on PS5 and Xbox Series X|S, "
           "$79.99. Set in Leonida's Vice City, starring Jason Duval and Lucia "
           "Caminos. A 99 Metascore (147 reviews); IGN and GameSpot both 10/10. "
           "Sensor Tower: 17.1m pre-orders, about $1.65bn.")
    text_block(d, left_x, 540, gta, mid_body, col_w, 26)

    d.text((right_x, 430), "MARKETS", font=kicker, fill=RED)
    d.text((right_x, 456), "ANT: THE BIGGEST IPO", font=mid_head, fill=INK)
    d.text((right_x, 494), "IN HISTORY", font=mid_head, fill=INK)
    # rising price chart beside the headline's second line, kept clear of
    # the first headline line (its glyphs end near y 489, x 950)
    chart = [(815, 534), (848, 520), (880, 528), (912, 510), (940, 496), (968, 486)]
    d.line(chart, fill=GREEN, width=3, joint="curve")
    d.polygon([(968, 486), (954, 490), (964, 500)], fill=GREEN)
    ipo = ("ANT began trading on Nasdaq today in the biggest IPO ever. Priced "
           "at $83 a share — above the $70–78 range — 980 million shares "
           "raised about $81.3bn at a $1.5 trillion valuation. First trade "
           "indicated 20%–26% above the offer price.")
    text_block(d, right_x, 540, ipo, mid_body, col_w, 26)

    d.line([(MARGIN, 710), (W - MARGIN, 710)], fill=INK, width=1)

    # ---------- third row: ICJ verdict / Hormuz tanker ----------
    d.line([(512, 720), (512, 886)], fill=GREY, width=1)
    small_head = font(SERIF_BOLD, 23)
    d.text((left_x, 720), "THE HAGUE", font=kicker, fill=RED)
    d.text((right_x, 720), "THE GULF", font=kicker, fill=RED)
    d.text((left_x, 746), "MYANMAR GUILTY OF GENOCIDE", font=small_head, fill=INK)
    d.text((right_x, 746), "TANKER STRUCK IN HORMUZ", font=small_head, fill=INK)
    icj = ("The ICJ ruled 9–6 that Myanmar committed genocide against the "
           "Rohingya in 2017 — the first time the court has found a state "
           "responsible. It ordered reparations.")
    text_block(d, left_x, 782, icj, mid_body, col_w, 26)
    hormuz = ("A tanker was hit overnight — an engine-room strike 6 nautical "
              "miles north of Khasab; the crew is safe. Iran claims two "
              "supertankers hit mines; the strait is effectively closed.")
    text_block(d, right_x, 782, hormuz, mid_body, col_w, 26)

    # ---------- ticker ----------
    d.rectangle([0, 896, W, 1012], fill=DARK)
    tick_font = font(SANS_BOLD, 18)
    tick_head = "AROUND THE WORLD"
    items = [
        "Israel's first ground op past Gaza's 'yellow line' since the "
        "ceasefire",
        "EU proposes €45bn loan for Ukraine",
        "House Democrats pick Jeffries for Speaker, 251–11; vote Jan 3",
        "Crimea bridge hit a third time in a week",
        "Bangladesh violence hits 28 districts; Yunus home torched",
    ]
    ticker_text = tick_head + "  ·  " + "  ·  ".join(items)
    lines = wrap(d, ticker_text, tick_font, W - 2 * MARGIN)
    y = 906
    for i, ln in enumerate(lines):
        if i == 0:
            hw = d.textlength(tick_head, font=tick_font)
            d.text((MARGIN, y), tick_head, font=tick_font, fill=TICKER_GOLD)
            d.text((MARGIN + hw, y), ln[len(tick_head):], font=tick_font, fill=WHITE)
        else:
            d.text((MARGIN, y), ln, font=tick_font, fill=WHITE)
        y += 24

    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
    print("lead body ends at y =", end_y, "| ticker lines:", len(lines))


if __name__ == "__main__":
    main()
