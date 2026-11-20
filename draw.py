#!/usr/bin/env python3
"""Render the make.fun news-image-20261120 v1 entry: one 1024x1024 PNG
summing up Friday 20 November 2026's world news. Written fresh in this
session. Deterministic: no clock, no randomness, no network.
Run: python3 draw.py [out.png]  (default entry.png next to this file)
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 241, 227)
INK = (26, 26, 26)
RED = (178, 34, 34)
RULE = (26, 26, 26)
PANEL = (255, 255, 255)
PANEL_LINE = (120, 110, 95)
SKY = (214, 232, 240)
LAND = (232, 214, 170)
LAND_LINE = (170, 150, 110)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap text; assert it fits in max_lines. Returns the lines."""
    lines = wrap(draw, text, fnt, max_w)
    assert len(lines) <= max_lines, f"OVERFLOW ({len(lines)}>{max_lines}): {text!r}"
    return lines


def draw_text(draw, xy, text, fnt, fill=INK, anchor="la"):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def centre(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx, y), text, font=fnt, fill=fill, anchor="ma")


# ---------------------------------------------------------------- stories
# Every story verified 20 Nov 2026 against its original source (see
# REPORT.md). Numbers are used in the list AND on the map.
HEROES = [
    dict(num=1, kicker="WAR", colour=(178, 34, 34),
         head="Russia fires 110 missiles at Kyiv in one night",
         cap="Over 400 drones join the barrage; 8 killed, three Dnipro "
             "bridges hit, and Russian missiles stray into Polish airspace.",
         art="kyiv"),
    dict(num=2, kicker="WEATHER", colour=(14, 110, 130),
         head="Akvan makes landfall in Odisha",
         cap="Cyclone crosses near Gopalpur at 80 km/h; 300,000+ sheltered, "
             "no deaths reported in the first count.",
         art="akvan"),
    dict(num=3, kicker="CLIMATE", colour=(14, 122, 107),
         head="COP31 ends its final day with no deal",
         cap="Antalya draft drops every fossil-fuel mention and the $120bn "
             "figure; Panama vows to block a weak text.",
         art="cop31"),
]

MIDS = [
    dict(num=4, kicker="MARKETS", colour=(178, 34, 34),
         head="ANT slides 11% on day two",
         cap="Anthropic falls to about $86 as the AI sell-off deepens; the "
             "debut's glow fades fast.",
         art="candles"),
    dict(num=5, kicker="CULTURE", colour=(107, 60, 140),
         head="GTA VI: 24.6m copies, $2.36bn",
         cap="Final day-one tally makes it the biggest entertainment launch "
             "ever.",
         art="gta"),
    dict(num=6, kicker="MARKETS", colour=(178, 34, 34),
         head="Wall Street heads for a 7th fall",
         cap="S&P on track for its worst week since April 2025 as the rout "
             "spreads to Asia.",
         art="falling"),
    dict(num=7, kicker="MARKETS", colour=(150, 110, 10),
         head="Gold sinks to $3,514",
         cap="A 14-month low as real rates surge; Bitcoin holds near $61,900, "
             "down 28% this quarter.",
         art="gold"),
    dict(num=8, kicker="ECONOMY", colour=(30, 100, 60),
         head="US mood lifts a little",
         cap="Consumer sentiment reaches 51.5; inflation fears ease to 3.7% "
             "for the year ahead.",
         art="consumer"),
    dict(num=9, kicker="IRAQ", colour=(140, 90, 20),
         head="Troops move on militia base",
         cap="Iraqi forces deploy to Jurf al-Sakhar, a Kataib Hezbollah "
             "stronghold.",
         art="iraq"),
    dict(num=10, kicker="DIPLOMACY", colour=(31, 78, 121),
         head="Putin invites Europe to Moscow",
         cap="Merz wants neutral ground; Kyiv a seat.",
         art="invite"),
    dict(num=11, kicker="SPORT", colour=(30, 100, 60),
         head="Marathon champion banned",
         cap="Jepchirchir loses her Sydney title; banned 3 years for doping.",
         art="runner"),
]

# also-on: label + one fact line each. Kept 50-70 chars where possible.
ALSO = [
    (12, "MOGADISHU", "Thousands rally backing the UAE envoy's expulsion."),
    (13, "META", "Muse reportedly read private encrypted messages."),
    (14, "CYBER CHIEF", "Trump ousts the cyber director after tech outages."),
    (15, "AI CHIPS", "US signed off on ~900,000 AI chips for China in 6 months."),
    (16, "TAIWAN", "Taiwan tells Meta thousands of China-linked accounts target votes."),
    (17, "SIGNAL", "Signal blocks screenshots to stop AI agents reading chats."),
    (18, "NUCLEAR", "Trump: arms limits with China and Russia \u201cvery hard\u201d."),
    (19, "RUSSIA ENERGY", "Moscow's fossil-fuel earnings at their highest since late 2022."),
    (20, "MEASLES", "US loses measles-free status as child vaccination rates fall."),
    (21, "YEMEN", "Saudis prepare for their Yemen campaign to last into 2027."),
    (22, "SEOUL", "Exam cheating scandal raises stakes in Korea's big test."),
    (23, "BRUSSELS", "EU strikes a deal to revamp sustainable finance rules."),
    (24, "MANAUS", "Amazon drought strands floating villages near Manaus."),
    (25, "SYDNEY", "NSW rejects $2bn+ airport metro claims; opening may slip to 2028."),
    (26, "DAVID JONES", "1,600 staff told their jobs end days after Christmas."),
    (27, "CANBERRA", "Sweeping defence laws pass with almost no debate."),
    (28, "SINGAPORE", "US Treasury presses Singapore and Malaysia on Iran sanctions."),
    (29, "COP31", "123 investors urge an ambitious deal on electrification."),
    (30, "EL NI\u00d1O", "UN: acting on El Ni\u00f1o now is cheaper than waiting."),
    (31, "AIR FORCE ONE", "Trump tells Europe it could save money by ending the war."),
    (32, "IPO", "Anthropic's debut is set to mint thousands of millionaires."),
    (33, "INDIA", "How India became a rice powerhouse \u2014 and why it's a problem."),
    (34, "YEARBOOK", "UN climate yearbook: only 44 of 96 indicators improving."),
    (35, "PANAMA", "Panama vows to block any COP31 deal without fossil fuels."),
    (36, "SHUTDOWN", "Congress faces a pre-Christmas shutdown fight on Iran."),
]

STRIP = [
    ("110+", "MISSILES FIRED AT KYIV"),
    ("300,000+", "AKVAN EVACUEES IN ODISHA"),
    ("24.6M", "GTA VI COPIES, DAY ONE"),
    ("\u221211%", "ANT SLIDES ON DAY TWO"),
    ("$3,514", "GOLD, A 14-MONTH LOW"),
    ("51.5", "US CONSUMER SENTIMENT"),
]

# map dots: (lon, lat, label, colour) — label lists every story at the dot.
CONT = {
    "ASIA": (192, 57, 43), "N. AMERICA": (31, 78, 121),
    "EUROPE": (14, 122, 107), "OCEANIA": (46, 125, 50),
    "AFRICA": (176, 124, 31), "S. AMERICA": (106, 61, 154),
}
DOTS = [
    (30.5, 50.5, "1", CONT["EUROPE"]),
    (84.9, 19.3, "2", CONT["ASIA"]),
    (30.7, 36.9, "3\u00b729\u00b734", CONT["EUROPE"]),
    (-74.0, 40.7, "4\u00b75\u00b76\u00b77\u00b78\u00b732", CONT["N. AMERICA"]),
    (-77.0, 38.9, "14\u00b715\u00b718\u00b736", CONT["N. AMERICA"]),
    (44.2, 32.9, "9", CONT["ASIA"]),
    (37.6, 55.8, "10\u00b719", CONT["EUROPE"]),
    (150.0, -34.5, "11\u00b725\u00b726\u00b727", CONT["OCEANIA"]),
    (45.3, 2.0, "12", CONT["AFRICA"]),
    (121.6, 25.0, "16", CONT["ASIA"]),
    (46.7, 24.7, "21", CONT["ASIA"]),
    (127.0, 37.5, "22", CONT["ASIA"]),
    (4.4, 50.8, "23", CONT["EUROPE"]),
    (-60.0, -3.1, "24", CONT["S. AMERICA"]),
    (103.8, 1.4, "28", CONT["ASIA"]),
    (77.2, 28.6, "33", CONT["ASIA"]),
    (-79.5, 9.0, "35", CONT["N. AMERICA"]),
]


# ---------------------------------------------------------------- art
def art_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 54))
    for sx, sy in [(0.12, 0.25), (0.3, 0.15), (0.5, 0.3), (0.7, 0.18), (0.88, 0.28)]:
        d.ellipse([x + sx * w - 2, y + sy * h - 2, x + sx * w + 2, y + sy * h + 2],
                  fill=(255, 255, 200))
    # explosions
    for cx, cy, r in [(0.22, 0.35, 16), (0.62, 0.28, 20), (0.85, 0.45, 13)]:
        ex, ey = x + cx * w, y + cy * h
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(255, 170, 40))
        d.ellipse([ex - r * 0.55, ey - r * 0.55, ex + r * 0.55, ey + r * 0.55],
                  fill=(255, 230, 120))
    # skyline + bridge
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(12, 12, 30))
    for bx in range(6):
        bw = w / 7
        bh = h * (0.18 + 0.1 * (bx % 3))
        d.rectangle([x + bx * (w / 6) + 4, y + h * 0.62 - bh,
                     x + bx * (w / 6) + 4 + bw, y + h * 0.62], fill=(40, 40, 80))
    d.rectangle([x, y + h * 0.86, x + w, y + h * 0.92], fill=(90, 90, 130))
    for px in range(5):
        px0 = x + (px + 0.5) * w / 5
        d.line([px0, y + h * 0.86, px0, y + h * 0.70], fill=(150, 150, 190), width=2)
    d.rectangle([x, y + h * 0.92, x + w, y + h], fill=(50, 80, 120))


def art_akvan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 170, 200))
    cx, cy = x + w * 0.5, y + h * 0.55
    for r, col in [(52, (255, 255, 255)), (40, (210, 235, 245)),
                   (28, (255, 255, 255)), (16, (170, 210, 230))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=5)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(240, 240, 240))
    # coastline + land
    d.polygon([(x, y + h), (x + w * 0.75, y + h), (x + w * 0.62, y + h * 0.55),
               (x + w * 0.45, y + h * 0.72), (x + w * 0.2, y + h * 0.6)],
              fill=(214, 190, 130))
    for rx in range(8):
        rx0 = x + rx * w / 8
        d.line([rx0, y + 6, rx0 + 8, y + h * 0.3], fill=(255, 255, 255), width=2)


def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 90, 80))
    # big sun with 1.5
    sx, sy = x + w * 0.78, y + h * 0.32
    d.ellipse([sx - 26, sy - 26, sx + 26, sy + 26], fill=(255, 200, 60))
    d.text((sx, sy), "1.5\u00b0", font=font(SANS_B, 15), fill=(120, 40, 0),
           anchor="mm")
    # podium + flags
    d.rectangle([x + w * 0.08, y + h * 0.62, x + w * 0.5, y + h * 0.68],
                fill=(240, 240, 230))
    d.rectangle([x + w * 0.24, y + h * 0.68, x + w * 0.34, y + h * 0.95],
                fill=(120, 60, 40))
    for fx, col in [(0.12, (220, 40, 40)), (0.30, (40, 90, 200)),
                    (0.48, (240, 240, 240))]:
        px = x + fx * w
        d.line([px, y + h * 0.18, px, y + h * 0.55], fill=(230, 230, 230), width=2)
        d.polygon([(px, y + h * 0.18), (px + 22, y + h * 0.25),
                   (px, y + h * 0.32)], fill=col)
    # empty chairs row
    for cx in range(4):
        cx0 = x + w * 0.58 + cx * w * 0.1
        d.rectangle([cx0, y + h * 0.7, cx0 + 16, y + h * 0.95], fill=(240, 220, 180))


def art_candles(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(252, 240, 240))
    pts = [0.25, 0.35, 0.3, 0.55, 0.7, 0.85]
    px = [x + (i + 0.5) * w / len(pts) for i in range(len(pts))]
    py = [y + v * h for v in pts]
    d.line(list(zip(px, py)), fill=(200, 40, 40), width=3)
    for i in range(len(pts) - 1):
        d.ellipse([px[i] - 4, py[i] - 4, px[i] + 4, py[i] + 4], fill=(200, 40, 40))
    d.text((x + w - 6, y + 4), "ANT", font=font(SANS_B, 13),
           fill=(200, 40, 40), anchor="ra")


def art_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 30, 90))
    sx, sy = x + w * 0.8, y + h * 0.3
    d.ellipse([sx - 18, sy - 18, sx + 18, sy + 18], fill=(255, 190, 80))
    d.text((x + w * 0.2, y + h * 0.18), "VI", font=font(SERIF, 34),
           fill=(255, 255, 255))
    d.rectangle([x, y + h * 0.68, x + w, y + h], fill=(20, 12, 40))
    for bx in range(7):
        bw = w / 8
        bh = h * (0.14 + 0.09 * ((bx * 7) % 4))
        d.rectangle([x + bx * (w / 7) + 2, y + h * 0.68 - bh,
                     x + bx * (w / 7) + 2 + bw, y + h * 0.68], fill=(70, 45, 120))
        for wy in range(2):
            d.rectangle([x + bx * (w / 7) + 6, y + h * 0.68 - bh + 4 + wy * 8,
                         x + bx * (w / 7) + 10, y + h * 0.68 - bh + 8 + wy * 8],
                        fill=(255, 220, 120))


def art_falling(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    pts = [(0.05, 0.2), (0.25, 0.3), (0.45, 0.28), (0.65, 0.55), (0.85, 0.75),
           (0.97, 0.9)]
    px = [x + a * w for a, _ in pts]
    py = [y + b * h for _, b in pts]
    d.line(list(zip(px, py)), fill=(200, 40, 40), width=3)
    d.polygon([(px[-1], py[-1]), (px[-1] - 14, py[-1] - 2), (px[-1] - 2, py[-1] - 14)],
              fill=(200, 40, 40))
    for gx in range(4):
        gy = y + (gx + 1) * h / 5
        d.line([x, gy, x + w, gy], fill=(230, 230, 230), width=1)


def art_gold(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 52, 32))
    for i, bx in enumerate([0.08, 0.32, 0.56]):
        d.polygon([(x + bx * w, y + h * 0.72), (x + (bx + 0.2) * w, y + h * 0.72),
                   (x + (bx + 0.16) * w, y + h * 0.45),
                   (x + (bx + 0.04) * w, y + h * 0.45)], fill=(230, 190, 60))
    cx, cy = x + w * 0.82, y + h * 0.5
    d.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(240, 180, 40),
              outline=(255, 230, 120), width=2)
    d.text((cx, cy), "\u20bf", font=font(SANS_B, 16), fill=(90, 60, 0), anchor="mm")


def art_consumer(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 245, 235))
    pts = [(0.08, 0.75), (0.3, 0.6), (0.5, 0.65), (0.72, 0.4), (0.94, 0.3)]
    px = [x + a * w for a, _ in pts]
    py = [y + b * h for _, b in pts]
    d.line(list(zip(px, py)), fill=(30, 120, 60), width=3)
    d.polygon([(px[-1], py[-1]), (px[-1] - 14, py[-1] + 2), (px[-1] - 2, py[-1] + 14)],
              fill=(30, 120, 60))
    d.text((x + 6, y + 4), "51.5", font=font(SANS_B, 14), fill=(30, 120, 60))


def art_iraq(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 196, 140))
    d.ellipse([x + w * 0.8, y + h * 0.2, x + w * 0.8 + 22, y + h * 0.2 + 22],
              fill=(255, 220, 130))
    for dx in range(4):
        dx0 = x + dx * w / 4
        d.line([dx0, y + h * 0.62, dx0 + w / 8, y + h * 0.5], fill=(160, 120, 70),
               width=3)
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(190, 155, 95))
    d.rectangle([x + w * 0.1, y + h * 0.5, x + w * 0.3, y + h * 0.62],
                fill=(120, 90, 60))
    d.rectangle([x + w * 0.62, y + h * 0.5, x + w * 0.9, y + h * 0.62],
                fill=(120, 90, 60))


def art_invite(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 238, 245))
    ex, ey, ew, eh = x + w * 0.1, y + h * 0.28, w * 0.62, h * 0.5
    d.rectangle([ex, ey, ex + ew, ey + eh], fill=(255, 255, 255),
                outline=(150, 150, 160), width=2)
    d.line([ex, ey, ex + ew / 2, ey + eh * 0.55], fill=(150, 150, 160), width=2)
    d.line([ex + ew, ey, ex + ew / 2, ey + eh * 0.55], fill=(150, 150, 160),
           width=2)
    d.ellipse([ex + ew / 2 - 8, ey + eh * 0.55 - 8, ex + ew / 2 + 8,
               ey + eh * 0.55 + 8], fill=(178, 34, 34))
    for tx in range(3):
        tx0 = x + w * 0.78
        d.rectangle([tx0, y + h * (0.2 + tx * 0.22), tx0 + 10,
                     y + h * (0.2 + tx * 0.22) + 26], fill=(120, 60, 60))
        d.polygon([(tx0 - 3, y + h * (0.2 + tx * 0.22)),
                   (tx0 + 13, y + h * (0.2 + tx * 0.22)),
                   (tx0 + 5, y + h * (0.2 + tx * 0.22) - 10)], fill=(200, 60, 60))


def art_runner(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 240))
    # harbour bridge arc
    d.arc([x + w * 0.05, y - h * 0.55, x + w * 0.95, y + h * 1.15], 180, 360,
          fill=(90, 90, 110), width=5)
    d.line([x + w * 0.05, y + h * 0.72, x + w * 0.95, y + h * 0.72],
           fill=(90, 90, 110), width=3)
    # runner: head, torso, limbs as thick lines
    hx, hy = x + w * 0.5, y + h * 0.32
    d.ellipse([hx - 6, hy - 6, hx + 6, hy + 6], fill=(30, 30, 30))
    d.line([hx, hy + 6, hx + 4, hy + 26], fill=(30, 30, 30), width=5)
    d.line([hx + 4, hy + 26, hx - 12, hy + 44], fill=(30, 30, 30), width=4)
    d.line([hx + 4, hy + 26, hx + 20, hy + 40], fill=(30, 30, 30), width=4)
    d.line([hx, hy + 12, hx - 14, hy + 4], fill=(30, 30, 30), width=4)
    d.line([hx, hy + 12, hx + 16, hy + 18], fill=(30, 30, 30), width=4)


ART = {"kyiv": art_kyiv, "akvan": art_akvan, "cop31": art_cop31,
       "candles": art_candles, "gta": art_gta, "falling": art_falling,
       "gold": art_gold, "consumer": art_consumer, "iraq": art_iraq,
       "invite": art_invite, "runner": art_runner}


def num_badge(d, cx, cy, num, r, fill, txt_fill=(255, 255, 255), fsize=13):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill,
              outline=(255, 255, 255), width=1)
    d.text((cx, cy), str(num), font=font(SANS_B, fsize), fill=txt_fill,
           anchor="mm")


# ---------------------------------------------------------------- layout
MX = 22  # side margin


def masthead(d, img):
    centre(d, W // 2, 10, "THE WORLD IN ONE DAY", font(SERIF, 46))
    centre(d, W // 2, 62, "Friday 20 November 2026", font(SERIF_R, 20),
           fill=(70, 70, 70))
    d.line([MX, 92, W - MX, 92], fill=RULE, width=2)
    centre(d, W // 2, 98, "36 STORIES \u00b7 6 CONTINENTS \u00b7 ONE PAGE",
           font(SANS_B, 15), fill=RED)


def strip(d, y0=122, h=46):
    cw = (W - 2 * MX - 5 * 8) / 6
    for i, (big, label) in enumerate(STRIP):
        x0 = MX + i * (cw + 8)
        d.rectangle([x0, y0, x0 + cw, y0 + h], outline=PANEL_LINE, width=1,
                    fill=PANEL)
        f_big = font(SANS_B, 17)
        # shrink the big number until the label fits on one line
        f_lab = font(SANS_B, 8)
        while d.textlength(label, font=f_lab) > cw - 8 and f_lab.size > 6:
            f_lab = font(SANS_B, f_lab.size - 1)
        centre(d, x0 + cw / 2, y0 + 3, big, f_big, fill=RED)
        centre(d, x0 + cw / 2, y0 + h - 14, label, f_lab)


def hero_panel(d, s, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=PANEL_LINE, width=1,
                fill=PANEL)
    ART[s["art"]](d, x0 + 1, y0 + 1, w - 2, 108)
    num_badge(d, x0 + 16, y0 + 124, s["num"], 11, s["colour"])
    d.text((x0 + 32, y0 + 117), s["kicker"], font=font(SANS_B, 11),
           fill=s["colour"])
    head = fit_lines(d, s["head"], font(SERIF, 19), w - 20, 2)
    yy = y0 + 136
    for ln in head:
        d.text((x0 + 10, yy), ln, font=font(SERIF, 19), fill=INK)
        yy += 23
    cap = fit_lines(d, s["cap"], font(SANS, 11), w - 20, 3)
    yy += 2
    for ln in cap:
        d.text((x0 + 10, yy), ln, font=font(SANS, 11), fill=(60, 60, 60))
        yy += 14


def mid_panel(d, s, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=PANEL_LINE, width=1,
                fill=PANEL)
    ART[s["art"]](d, x0 + 1, y0 + 1, w - 2, 34)
    num_badge(d, x0 + 14, y0 + 47, s["num"], 10, s["colour"], fsize=11)
    d.text((x0 + 28, y0 + 41), s["kicker"], font=font(SANS_B, 9),
           fill=s["colour"])
    head = fit_lines(d, s["head"], font(SERIF, 13), w - 14, 2)
    yy = y0 + 54
    for ln in head:
        d.text((x0 + 7, yy), ln, font=font(SERIF, 13), fill=INK)
        yy += 15
    cap = fit_lines(d, s["cap"], font(SANS, 9), w - 14, 2)
    for ln in cap:
        d.text((x0 + 7, yy), ln, font=font(SANS, 9), fill=(60, 60, 60))
        yy += 11
    assert yy <= y0 + h - 4, f"mid overflow #{s['num']}: {yy} > {y0 + h - 4}"


# simplified continent outlines (lon, lat), equirectangular
CONTINENTS = {
    "NA": [(-168, 66), (-150, 70), (-130, 71), (-110, 73), (-95, 80),
           (-85, 66), (-78, 71), (-65, 60), (-55, 52), (-60, 46),
           (-70, 42), (-75, 35), (-80, 32), (-85, 30), (-90, 21),
           (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49),
           (-140, 60), (-155, 58), (-165, 60)],
    "SA": [(-80, 10), (-75, 5), (-70, -5), (-60, -10), (-50, -5),
           (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -40),
           (-70, -50), (-73, -40), (-70, -20), (-75, -15), (-80, -5)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57),
           (10, 59), (18, 56), (21, 55), (24, 59), (28, 60), (30, 62),
           (25, 65), (20, 70), (15, 68), (10, 64), (5, 60), (0, 55),
           (-5, 50), (-10, 44)],
    "AF": [(-6, 35), (-10, 30), (-15, 20), (-17, 12), (-12, 5), (-8, 0),
           (9, -1), (12, -5), (13, -12), (12, -18), (16, -25), (20, -30),
           (28, -33), (32, -28), (35, -22), (40, -15), (42, -10),
           (48, -5), (51, 2), (50, 10), (44, 12), (40, 15), (38, 20),
           (35, 28), (30, 32), (22, 33), (15, 32), (10, 37)],
    "AS": [(28, 45), (35, 48), (40, 50), (45, 51), (50, 52), (55, 55),
           (60, 58), (65, 62), (70, 66), (75, 70), (85, 72), (95, 74),
           (105, 75), (115, 73), (125, 71), (135, 70), (145, 71),
           (155, 68), (162, 62), (158, 55), (152, 58), (145, 54),
           (140, 47), (135, 42), (128, 38), (124, 32), (120, 26),
           (113, 22), (109, 15), (106, 9), (101, 7), (98, 10), (94, 16),
           (91, 22), (87, 21), (83, 17), (80, 13), (77, 8), (74, 18),
           (71, 22), (67, 24), (62, 25), (58, 25), (54, 26), (50, 28),
           (47, 30), (44, 29), (40, 31), (36, 33), (33, 35), (30, 38),
           (28, 42)],
    "OC": [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
           (130, -32), (132, -30), (135, -28), (140, -25), (142, -20),
           (142, -15), (140, -12), (136, -12), (132, -12), (130, -13),
           (126, -14), (122, -17), (118, -20)],
}
# badge offsets (dx, dy px) to keep close dots apart; leader line drawn.
# Positions were hand-checked against the equal-aspect projection so no
# two badges overlap (Europe/ME cluster and the NYC/DC pair fan out).
OFFSETS = {"1": (-12, -12), "10\u00b719": (16, -14),
           "3\u00b729\u00b734": (-16, 16), "23": (-14, -8), "9": (12, 8),
           "21": (18, 22), "12": (0, 6), "33": (-14, -10),
           "14\u00b715\u00b718\u00b736": (-24, 18), "35": (0, 12),
           "24": (8, 0), "22": (8, -18), "16": (10, -10), "28": (12, 8)}


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=PANEL_LINE, width=1,
                fill=SKY)
    d.text((x0 + 8, y0 + 6), "WHERE IT HAPPENED", font=font(SANS_B, 12),
           fill=INK)
    d.line([x0 + 8, y0 + 24, x0 + w - 8, y0 + 24], fill=RULE, width=1)

    # equal px-per-degree on both axes (no vertical stretch), letterboxed
    # in the panel so the world keeps its true shape
    scale = min((w - 12) / 360, (h - 38) / 142)
    voff = ((h - 38) - 142 * scale) / 2

    def proj(lon, lat):
        px = x0 + 6 + (lon + 170) * scale
        py = y0 + 30 + voff + (84 - lat) * scale
        return px, py

    for pts in CONTINENTS.values():
        d.polygon([proj(lo, la) for lo, la in pts], fill=LAND,
                  outline=LAND_LINE)
    # markers
    f_dot = font(SANS_B, 8)
    for lon, lat, label, col in DOTS:
        px, py = proj(lon, lat)
        dx, dy = OFFSETS.get(label, (0, 0))
        bx, by = px + dx, py + dy
        if (dx, dy) != (0, 0):
            d.line([px, py, bx, by], fill=(90, 90, 90), width=1)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(60, 60, 60))
        # badge sized to the label
        tw = d.textlength(label, font=f_dot) + 8
        bw = max(16, tw)
        d.rounded_rectangle([bx - bw / 2, by - 8, bx + bw / 2, by + 8],
                            radius=8, fill=col, outline=(255, 255, 255),
                            width=1)
        d.text((bx, by), label, font=f_dot, fill=(255, 255, 255), anchor="mm")
    # legend
    lx, ly = x0 + 8, y0 + h - 34
    items = [("ASIA", CONT["ASIA"]), ("N. AMER.", CONT["N. AMERICA"]),
             ("EUROPE", CONT["EUROPE"]), ("OCEANIA", CONT["OCEANIA"]),
             ("AFRICA", CONT["AFRICA"]), ("S. AMER.", CONT["S. AMERICA"])]
    xx = lx
    f_leg = font(SANS_B, 7)
    for name, col in items:
        d.ellipse([xx, ly, xx + 7, ly + 7], fill=col)
        d.text((xx + 10, ly - 1), name, font=f_leg, fill=INK)
        xx += 10 + d.textlength(name, font=f_leg) + 5
    d.text((lx, ly + 13), "13 = CALIFORNIA \u00b7 17\u00b720 = USA \u00b7 30 = GLOBAL \u00b7 "
           "31 = AIR FORCE ONE", font=font(SANS, 8), fill=(70, 70, 70))


def also_on(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=PANEL_LINE, width=1,
                fill=PANEL)
    d.text((x0 + 10, y0 + 6), "ALSO ON FRIDAY 20 NOVEMBER",
           font=font(SANS_B, 12), fill=INK)
    d.line([x0 + 10, y0 + 24, x0 + w - 10, y0 + 24], fill=RULE, width=1)
    cols = [ALSO[0:9], ALSO[9:17], ALSO[17:25]]
    cw = (w - 20) / 3
    f_lab = font(SANS_B, 9)
    f_txt = font(SANS, 8)
    for ci, col in enumerate(cols):
        cx = x0 + 10 + ci * cw
        yy = y0 + 32
        for num, label, text in col:
            num_badge(d, cx + 8, yy + 6, num, 8, RED, fsize=9)
            full = label + " \u2014 " + text
            lines = fit_lines(d, full, f_txt, cw - 30, 2)
            ly = yy
            for li, ln in enumerate(lines):
                if li == 0:
                    # bold label, regular remainder on the first line
                    d.text((cx + 20, ly), label, font=f_lab, fill=RED)
                    rest = ln[len(label):]
                    d.text((cx + 20 + d.textlength(label, font=f_lab), ly),
                           rest, font=f_txt, fill=INK)
                else:
                    d.text((cx + 20, ly), ln, font=f_txt, fill=INK)
                ly += 10
            yy = ly + 4
    assert yy <= y0 + h - 4, f"also-on overflow: {yy} > {y0 + h - 4}"


def footer(d, y0):
    d.line([MX, y0, W - MX, y0], fill=RULE, width=2)
    centre(d, W // 2, y0 + 6,
           "Every story here happened or was first reported on "
           "Friday 20 November 2026.",
           font(SANS_B, 11))
    centre(d, W // 2, y0 + 22,
           "Sources: Reuters, UN News, IMD, Univ. of Michigan, CoinDesk, "
           "Sensor Tower, ABC. Original drawings.",
           font(SANS, 9), fill=(90, 90, 90))


def render(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d, img)
    strip(d)
    # heroes: 3 across
    hw = (W - 2 * MX - 2 * 10) / 3
    for i, s in enumerate(HEROES):
        hero_panel(d, s, MX + i * (hw + 10), 176, hw, 244)
    # mids: 2 rows x 4
    mw = (W - 2 * MX - 3 * 8) / 4
    for i, s in enumerate(MIDS):
        r, c = divmod(i, 4)
        mid_panel(d, s, MX + c * (mw + 8), 428 + r * 106, mw, 100)
    # bottom band
    map_w = 316
    draw_map(d, MX, 648, map_w, 306)
    also_on(d, MX + map_w + 10, 648, W - MX - (MX + map_w + 10), 306)
    footer(d, 962)
    img.save(out_path, "PNG")
    return out_path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render(out)
    print("wrote", out, os.path.getsize(out), "bytes")
