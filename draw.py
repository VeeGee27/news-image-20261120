"""Renders the Friday 20 November 2026 front page (1024x1024, deterministic).

Build-time renderer only: Pillow is used here, never by main.py.
All artwork is drawn with vector shapes; no external assets.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 28
CW = W - 2 * M

PAPER = (247, 242, 231)
INK = (22, 21, 19)
RED = (168, 30, 34)
NAVY = (22, 35, 63)
MUTED = (107, 100, 85)
FAINT = (201, 191, 169)
BAND = (238, 232, 218)
MAPLAND = (203, 191, 154)
MAPLBL = (143, 163, 200)
WHITE = (255, 255, 255)
GREEN = (46, 125, 50)

FD = "/usr/share/fonts/truetype/dejavu"


def F(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)

# ---------------------------------------------------------------- stories
# Drawn stories are numbered 1-13 (3 heroes + 10 mids); briefs 14-36.
# (headline, kicker, deck, source, tag, lat, lon, region)
HEROES = [
    ("KYIV", "1 KYIV, UKRAINE · WAR", "OFFICIALS' COUNT",
     "Russian missiles hit three Kyiv bridges",
     "An overnight barrage of about 110 missiles and 400 drones killed "
     "at least eight people; three Dnipro bridges hit; power cut in "
     "five districts. (Reuters)",
     50.45, 30.52, "Europe"),
    ("CYCLONE AKVAN", "2 ODISHA, INDIA · CYCLONE", "WEATHER OFFICE",
     "Cyclone Akvan comes ashore in eastern India",
     "The storm crossed the coast near Gopalpur at 02:00–03:00 UTC; "
     "372,000 people were moved to 9,341 shelters. No deaths "
     "reported. (IMD, Deccan Herald)",
     19.27, 84.92, "Asia"),
    ("COP31: NO DEAL", "3 ANTALYA, TÜRKIYE · CLIMATE", "ONGOING · UN NEWS",
     "COP31 reaches its last day with no deal",
     "The draft text leaves out fossil fuels and the $120bn adaptation "
     "figure; Panama objects and talks spill to the weekend. "
     "(Carbon Brief)",
     36.90, 30.70, "Global"),
]

MIDS = [
    ("4 TOKYO · MARKETS", "CONFIRMED · REUTERS",
     "AI sell-off sinks Asian shares",
     "Nikkei −4.2% Friday; TSMC −$63bn, SoftBank −16%.",
     35.68, 139.69, "Asia", "chart"),
    ("5 BRUSSELS · DIPLOMACY", "REPORTED · REUTERS",
     "UK and EU seal a “reset” deal",
     "Food trade, youth visas, carbon link; worth £5.1bn a year.",
     50.85, 4.35, "Europe", "flags"),
    ("6 NEW YORK · TECH", "CONFIRMED · CNBC/AP",
     "Anthropic slides after debut",
     "Day after its $81.3bn debut, shares fall as AI doubts spread.",
     40.71, -74.01, "N. America", "chip"),
    ("7 E. POLAND · SECURITY", "OFFICIAL · WARSAW",
     "Russian missiles land in Poland",
     "2 missiles, 1 drone cross overnight; no one hurt.",
     51.25, 22.57, "Europe", "missile"),
    ("8 IRAQ · SECURITY", "REPORTED · JUST SECURITY",
     "Iraqi army enters militia stronghold",
     "Troops deploy in Jurf al-Sakhar against Iran-backed Kataib "
     "Hezbollah.",
     32.85, 44.20, "Asia", "tanks"),
    ("9 TALLINN · SECURITY", "OFFICIAL · JUST SECURITY",
     "Estonia shuts Russia border",
     "Crossings close for at least six months.",
     59.44, 24.75, "Europe", "border"),
    ("10 ROME · LABOUR", "REPORTED · FRANCE 24",
     "General strike over Italy’s budget",
     "Workers and students march over wages and living costs.",
     41.90, 12.50, "Europe", "march"),
    ("11 ROME · TECH", "REPORTED · MORNING BRIEFING",
     "Meta fined €805m in Italy",
     "Italy fines Meta over Android photo access; Meta says it will "
     "appeal.",
     41.90, 12.50, "Europe", "scales"),
    ("12 NEW YORK · MARKETS", "CONFIRMED · REUTERS",
     "S&P 500 falls 2% again",
     "Fifth straight day of losses as the AI rout spreads to US "
     "stocks.",
     40.71, -74.01, "N. America", "sp500"),
    ("13 JAKARTA · CLIMATE", "REPORTED · THE HINDU",
     "Indonesia fires may cost $30bn",
     "Losses could reach $30bn as haze spreads.",
     -6.21, 106.85, "Asia", "fire"),
]

# (number, location, text, source, lat, lon, region)
BRIEFS = [
    (14, "AVARUA", "Cyclone Xavier emergency declared", "RNZ", -21.24, -159.78, "Oceania"),
    (15, "WASHINGTON", "Energy bill 62–33", "BANGLADESH CHRONICLE", 38.90, -77.04, "N. America"),
    (16, "NEW YORK", "Grid fix pegged at $1tn", "MARTIN LUMEN", 40.71, -74.01, "N. America"),
    (17, "WASHINGTON", "Cyber chief exits", "BANGLADESH CHRONICLE", 38.90, -77.04, "N. America"),
    (18, "RICHMOND", "Virginia quits tax plan", "MORNING BRIEFING", 37.54, -77.44, "N. America"),
    (19, "CALIFORNIA", "Coinbase eyes predictions", "MARTIN LUMEN", 37.77, -122.42, "N. America"),
    (20, "TEGUCIGALPA", "Honduras raises $375m", "LATIN LAWYER", 14.08, -87.21, "N. America"),
    (21, "SANTIAGO", "Chile–Philippines pact", "LATAM CHRONICLE", -33.45, -70.67, "S. America"),
    (22, "LIMA", "Cheiron enters Peru oil block", "LATIN LAWYER", -12.05, -77.04, "S. America"),
    (23, "PESHAWAR", "22 militants dead", "BANGLADESH CHRONICLE", 34.02, 71.58, "Asia"),
    (24, "DHAKA", "Bangladesh tense", "BANGLADESH CHRONICLE", 23.81, 90.41, "Asia"),
    (25, "KUALA LUMPUR", "10,000 Rohingya to resettle", "MARTIN LUMEN", 3.14, 101.69, "Asia"),
    (26, "PARIS", "Data centres may lift emissions", "MORNING BRIEFING", 48.86, 2.35, "Europe"),
    (27, "BEIJING", "China spies used zero-day", "MORNING BRIEFING", 39.90, 116.41, "Asia"),
    (28, "PRETORIA", "~600 women killed in 3 months", "AL JAZEERA", -25.75, 28.19, "Africa"),
    (29, "JOHANNESBURG", "Court eyes Lindela detention", "FRANCE 24", -26.20, 28.05, "Africa"),
    (30, "ACCRA", "Ghana’s $60m jet purchase sparks row", "MARTIN LUMEN", 5.60, -0.19, "Africa"),
    (31, "ABUJA", "Nigeria ends jail for suicide attempts", "MARTIN LUMEN", 9.06, 7.49, "Africa"),
    (32, "LAGOS", "Deaf Nigerians embrace sign languages", "THE GUARDIAN", 6.52, 3.38, "Africa"),
    (33, "SOUTHLAND", "Storm review: poor comms, stretched staff", "RNZ", -46.41, 168.35, "Oceania"),
    (34, "WELLINGTON", "NZ Defence Force database breached", "RNZ", -41.29, 174.78, "Oceania"),
    (35, "SYDNEY", "ASX −1.58% in the AI rout", "THE GUARDIAN", -33.87, 151.21, "Oceania"),
    (36, "BERLIN", "Youth strike in 25+ countries over living costs", "CNN", 52.52, 13.40, "Europe"),
]

STATS = [
    ("27", "ballistic missiles fired at Kyiv overnight"),
    ("9,341", "shelters housing Akvan evacuees"),
    ("−4.2%", "Nikkei, Friday’s close"),
    ("£5.1bn", "UK–EU deal value, a year"),
    ("100,000", "youth visas a year, UK–EU deal"),
    ("0", "fossil-fuel mentions in COP31 draft"),
]

REGIONS = [
    ("EUROPE", 8, (31, 78, 121)),
    ("ASIA", 8, (179, 84, 30)),
    ("N. AMERICA", 8, (46, 125, 50)),
    ("S. AMERICA", 2, (123, 94, 167)),
    ("AFRICA", 5, (138, 109, 27)),
    ("OCEANIA", 4, (14, 124, 123)),
    ("GLOBAL", 1, (85, 85, 85)),
]


def wrap(draw, text, font, width):
    """Greedy word wrap; returns a list of lines that fit width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, font, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y

# ------------------------------------------------------------------- map
# Simplified continent outlines as (lon, lat) points.
LAND = [
    [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60), (-135, 58),
     (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24),
     (-105, 20), (-97, 16), (-94, 17), (-90, 14), (-86, 12), (-83, 9),
     (-79, 9), (-81, 13), (-83, 15), (-87, 16), (-88, 18), (-90, 21),
     (-91, 19), (-96, 19), (-97, 22), (-97, 26), (-93, 30), (-89, 30),
     (-84, 30), (-81, 25), (-80, 32), (-76, 35), (-74, 40), (-70, 42),
     (-68, 45), (-65, 44), (-60, 47), (-55, 52), (-60, 55), (-65, 58),
     (-68, 58), (-72, 62), (-78, 62), (-85, 66), (-92, 66), (-95, 69),
     (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68)],
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50), (-70, -54),
     (-66, -55), (-68, -50), (-65, -45), (-62, -40), (-57, -35), (-52, -32),
     (-48, -28), (-41, -23), (-39, -17), (-35, -8), (-35, -5), (-40, -3),
     (-44, -2), (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11),
     (-72, 12), (-76, 10)],
    [(-17, 15), (-16, 20), (-15, 25), (-10, 31), (-5, 35), (0, 36),
     (10, 37), (11, 34), (20, 32), (30, 31), (32, 31), (34, 28), (35, 24),
     (37, 22), (39, 18), (40, 15), (43, 11), (48, 11), (51, 12), (46, 5),
     (42, 0), (40, -5), (38, -10), (35, -18), (32, -26), (28, -33),
     (20, -35), (17, -32), (15, -27), (12, -18), (13, -12), (12, -6),
     (9, 4), (4, 6), (-2, 5), (-8, 4), (-13, 8), (-17, 12)],
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50),
     (0, 50), (3, 52), (7, 54), (8, 57), (10, 59), (5, 60), (5, 62),
     (10, 64), (12, 66), (18, 69), (25, 71), (32, 70), (40, 68), (50, 69),
     (60, 69), (70, 72), (80, 73), (90, 75), (100, 76), (110, 74),
     (120, 73), (130, 72), (140, 72), (150, 70), (160, 70), (170, 67),
     (178, 65), (170, 60), (162, 56), (158, 52), (150, 60), (142, 55),
     (140, 50), (135, 44), (130, 42), (127, 40), (122, 38), (120, 32),
     (118, 25), (110, 20), (108, 12), (105, 9), (100, 8), (98, 12),
     (94, 16), (92, 21), (89, 22), (86, 20), (82, 17), (80, 13), (77, 8),
     (75, 12), (72, 20), (68, 23), (66, 25), (61, 25), (57, 26), (52, 26),
     (50, 29), (48, 30), (44, 29), (40, 31), (36, 36), (33, 36), (30, 36),
     (27, 37), (23, 36), (19, 40), (15, 40), (12, 44), (8, 44), (3, 43),
     (0, 40), (-2, 37), (-6, 36), (-9, 37)],
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (140, 36),
     (141, 38), (141, 41), (142, 44), (144, 44), (143, 42), (140, 40),
     (139, 37), (137, 35), (135, 33), (132, 33)],
    [(95, 5), (98, 4), (100, 0), (102, -3), (104, -5), (106, -6),
     (108, -7), (110, -7), (112, -7), (114, -8), (116, -9), (119, -9),
     (120, -10), (122, -9), (124, -10), (126, -9), (128, -8), (130, -7),
     (131, -4), (132, -2), (134, -3), (136, -4), (138, -5), (140, -7),
     (141, -8), (138, -8), (136, -7), (134, -5), (132, -3), (130, -2),
     (128, 0), (126, 1), (124, 1), (122, 2), (120, 1), (118, 0), (116, 1),
     (114, 3), (112, 3), (110, 1), (108, 0), (106, -1), (104, 1),
     (102, 3), (100, 5)],
    [(113, -22), (114, -30), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (147, -39),
     (150, -37), (153, -32), (153, -27), (151, -24), (149, -20), (146, -19),
     (143, -15), (142, -11), (140, -17), (136, -15), (135, -12), (132, -12),
     (130, -13), (127, -14), (125, -16), (122, -17), (120, -20), (116, -21)],
    [(167, -45), (168, -44), (170, -42), (172, -41), (174, -39), (176, -38),
     (178, -37), (176, -39), (174, -41), (172, -43), (170, -45), (168, -46),
     (167, -46)],
    [(131, -1), (134, -2), (137, -3), (140, -4), (143, -5), (146, -6),
     (148, -8), (150, -9), (147, -9), (144, -8), (141, -8), (138, -7),
     (135, -5), (132, -3)],
    [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (45, -25),
     (43, -22), (44, -18)],
    [(-55, 60), (-52, 60), (-48, 62), (-45, 60), (-40, 62), (-35, 65),
     (-30, 68), (-25, 70), (-22, 72), (-20, 74), (-25, 76), (-30, 78),
     (-40, 80), (-50, 80), (-58, 76), (-60, 72), (-58, 68), (-55, 64)],
    [(-22, 64), (-18, 63), (-15, 64), (-14, 66), (-18, 66), (-22, 65)],
]

# Badge offsets (dx, dy in px) for clustered pins; keyed by story number.
PIN_OFF = {
    5: (-16, -12), 6: (0, -14), 7: (16, -12), 9: (-14, -14),
    10: (0, -13), 11: (0, 13),
    12: (17, 12), 15: (-19, -13), 16: (-17, 13), 17: (19, -13),
    18: (0, 14), 26: (13, 11), 28: (0, -13), 29: (0, 13),
    31: (-15, 0), 32: (15, 0), 33: (-13, 9), 34: (11, -9),
}

LAT_TOP, LAT_BOT = 84.0, -56.0


def project(lon, lat, mx, my, mw, mh):
    x = mx + (lon + 180.0) / 360.0 * mw
    y = my + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * mh
    return x, y


# ------------------------------------------------------------- illustrations
def hero_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 46))
    # stars
    for sx, sy in [(18, 12), (52, 26), (96, 10), (150, 20), (210, 8),
                   (262, 22), (296, 12), (120, 34), (240, 34)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                  fill=(220, 220, 200))
    # skyline
    for bx, bw, bh in [(0, 34, 34), (40, 26, 48), (72, 40, 30), (118, 30, 52),
                       (154, 36, 36), (196, 28, 46), (230, 34, 32),
                       (270, 30, 44)]:
        d.rectangle([x + bx, y + h - bh - 26, x + bx + bw, y + h - 26],
                    fill=(8, 12, 24))
        for wy in range(y + h - bh - 20, y + h - 30, 9):
            for wx in range(x + bx + 5, x + bx + bw - 4, 10):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 120))
    # river + bridge deck
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(28, 52, 86))
    d.rectangle([x, y + h - 34, x + w, y + h - 28], fill=(200, 200, 190))
    # broken span: right half of the deck tilts down
    d.polygon([(x + w * 0.52, y + h - 34), (x + w, y + h - 22),
               (x + w, y + h - 16), (x + w * 0.52, y + h - 28)],
              fill=(150, 150, 140))
    for ax in (0.16, 0.34):
        d.arc([x + w * ax - 26, y + h - 62, x + w * ax + 26, y + h - 28],
              180, 360, fill=(200, 200, 190), width=3)
    # missile trails: dashed diagonals from top right to the bridge
    for (tx, ty, ix) in [(300, 2, 250), (250, 0, 180), (205, 4, 120)]:
        px, py = x + tx, y + ty
        ex, ey = x + ix, y + h - 34
        steps = 14
        for i in range(steps):
            if i % 2 == 0:
                continue
            t0, t1 = i / steps, (i + 0.7) / steps
            d.line([(px + (ex - px) * t0, py + (ey - py) * t0),
                    (px + (ex - px) * t1, py + (ey - py) * t1)],
                   fill=(255, 220, 130), width=3)
        # impact burst
        for (dx, dy, r) in [(0, 0, 11), (-8, -5, 6), (8, -6, 6), (0, -10, 5)]:
            d.ellipse([ex + dx - r, ey + dy - r, ex + dx + r, ey + dy + r],
                      fill=(255, 170, 40))
        d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(255, 240, 180))
    # smoke plumes
    for (sx, sy, r) in [(250, 66, 9), (258, 58, 7), (180, 70, 8),
                        (188, 62, 6)]:
        d.ellipse([x + sx - r, y + sy - r, x + sx + r, y + sy + r],
                  fill=(120, 120, 118))


def hero_akvan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 90, 110))
    # land strip top-left
    d.polygon([(x, y), (x + 108, y), (x + 88, y + 58), (x, y + 66)],
              fill=(203, 191, 154))
    d.text((x + 10, y + 8), "ODISHA", font=SANS_B(10), fill=(60, 50, 30))
    d.text((x + 10, y + 22), "GOPALPUR", font=SANS_B(9), fill=(60, 50, 30))
    d.ellipse([x + 96 - 4, y + 44 - 4, x + 96 + 4, y + 44 + 4], fill=RED)
    # cyclone spiral: concentric arcs around a centre
    cx, cy = x + 205, y + 62
    for r, a0, a1 in [(52, 20, 300), (40, 110, 30), (28, 200, 120),
                     (16, 290, 210)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=WHITE, width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 220, 130))
    # rain slashes
    for rx in range(x + 8, x + w - 8, 26):
        d.line([(rx, y + h - 26), (rx - 6, y + h - 12)], fill=(200, 225, 235),
               width=2)
    # wave lines
    for wy in (y + h - 34, y + h - 22, y + h - 10):
        d.line([(x + 130, wy), (x + w - 10, wy)], fill=(140, 190, 205),
               width=2)


def hero_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 218))
    # globe
    cx, cy, r = x + 62, y + 56, 42
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 110, 160))
    d.ellipse([cx - 26, cy - 30, cx - 2, cy - 8], fill=(90, 160, 90))
    d.ellipse([cx + 4, cy + 6, cx + 28, cy + 30], fill=(90, 160, 90))
    d.ellipse([cx - 14, cy + 12, cx + 8, cy + 34], fill=(70, 140, 80))
    d.arc([cx - r, cy - r, cx + r, cy + r], 0, 360, fill=(22, 21, 19), width=2)
    # thermometer
    tx = x + 150
    d.rounded_rectangle([tx, y + 14, tx + 16, y + 78], radius=8,
                        outline=INK, width=2, fill=WHITE)
    d.ellipse([tx - 6, y + 74, tx + 22, y + 96], outline=INK, width=2,
              fill=RED)
    d.rectangle([tx + 5, y + 30, tx + 11, y + 80], fill=RED)
    # NO DEAL stamp
    d.rectangle([x + 196, y + 18, x + 300, y + 46], fill=RED)
    d.text((x + 206, y + 24), "NO DEAL", font=SANS_B(16), fill=WHITE)
    d.text((x + 196, y + 56), "FINAL DAY", font=SANS_B(13), fill=INK)
    d.text((x + 196, y + 76), "ANTALYA", font=SANS_B(11), fill=MUTED)


def mid_art(d, kind, x, y, w, h):
    """Small monochrome illustration band for a mid card."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 212))
    if kind == "chart":
        d.line([(x + 12, y + h - 14), (x + w - 12, y + h - 14)],
               fill=MUTED, width=1)
        pts = [(x + 14, y + 14), (x + 52, y + 22), (x + 90, y + 18),
               (x + 128, y + 34), (x + 168, y + 40)]
        d.line(pts, fill=RED, width=3)
        d.ellipse([pts[-1][0] - 3, pts[-1][1] - 3, pts[-1][0] + 3,
                   pts[-1][1] + 3], fill=RED)
    elif kind == "flags":
        # EU flag
        d.rectangle([x + 16, y + 10, x + 76, y + h - 10], fill=(31, 62, 120))
        for i in range(8):
            import math
            a = i * 3.14159 / 4
            d.ellipse([x + 46 + 11 * math.cos(a) - 1,
                       y + h // 2 + 9 * math.sin(a) - 1,
                       x + 46 + 11 * math.cos(a) + 1,
                       y + h // 2 + 9 * math.sin(a) + 1],
                      fill=(255, 220, 80))
        # UK flag (simplified cross)
        d.rectangle([x + 96, y + 10, x + 168, y + h - 10], fill=(30, 60, 140))
        d.rectangle([x + 128, y + 10, x + 136, y + h - 10], fill=WHITE)
        d.rectangle([x + 96, y + h // 2 - 4, x + 168, y + h // 2 + 4],
                    fill=WHITE)
        d.rectangle([x + 130, y + 10, x + 134, y + h - 10], fill=RED)
        d.rectangle([x + 96, y + h // 2 - 2, x + 168, y + h // 2 + 2],
                    fill=RED)
    elif kind == "chip":
        d.rectangle([x, y, x + w, y + h], fill=(22, 35, 63))
        d.rectangle([x + 70, y + 10, x + 116, y + h - 10], fill=(46, 160, 90))
        d.rectangle([x + 82, y + 20, x + 104, y + h - 20], fill=(22, 35, 63))
        for px in (76, 88, 100):
            d.line([(x + px, y + 4), (x + px, y + 10)], fill=(200, 200, 200),
                   width=2)
            d.line([(x + px, y + h - 10), (x + px, y + h - 4)],
                   fill=(200, 200, 200), width=2)
    elif kind == "missile":
        d.rectangle([x, y, x + w, y + h], fill=(120, 150, 90))
        d.polygon([(x + 78, y + 6), (x + 94, y + 28), (x + 82, y + 28)],
                  fill=(240, 240, 230))
        d.rectangle([x + 80, y + 28, x + 92, y + 46], fill=(240, 240, 230))
        d.line([(x + 86, y + 6), (x + 150, y + 6)], fill=(255, 220, 130),
               width=2)
        for dx in range(0, 60, 12):
            d.line([(x + 96 + dx, y + 10), (x + 102 + dx, y + 10)],
                   fill=(255, 220, 130), width=2)
        d.line([(x + 20, y + h - 8), (x + 160, y + h - 8)], fill=(60, 90, 50),
               width=3)
        for gx in range(x + 14, x + w - 10, 22):
            d.line([(gx, y + h - 8), (gx + 4, y + h - 16)], fill=(60, 90, 50),
                   width=2)
    elif kind == "tanks":
        d.rectangle([x, y, x + w, y + h], fill=(210, 200, 170))
        for tx in (18, 76, 134):
            d.rectangle([x + tx, y + 22, x + tx + 44, y + 36], fill=(70, 70, 66))
            d.line([(x + tx + 34, y + 26), (x + tx + 56, y + 18)], fill=(70, 70, 66),
                   width=4)
            for wx in (tx + 6, tx + 18, tx + 30):
                d.ellipse([x + wx, y + 36, x + wx + 9, y + 45], fill=INK)
    elif kind == "border":
        d.rectangle([x, y, x + w, y + h], fill=(232, 226, 212))
        for px in range(x + 12, x + w - 8, 26):
            d.line([(px, y + 8), (px, y + h - 8)], fill=INK, width=3)
        d.rectangle([x + 8, y + 12, x + w - 8, y + 20], fill=RED)
        d.rectangle([x + 8, y + 30, x + w - 8, y + 38], fill=WHITE,
                    outline=INK)
    elif kind == "march":
        d.rectangle([x, y, x + w, y + h], fill=(232, 226, 212))
        for px, ph in [(30, 26), (62, 32), (94, 26), (126, 32), (156, 26)]:
            d.ellipse([x + px - 6, y + 8, x + px + 6, y + 20], fill=INK)
            d.polygon([(x + px - 8, y + h - 8), (x + px - 8, y + 22),
                       (x + px + 8, y + 22), (x + px + 8, y + h - 8)],
                      fill=INK)
        d.rectangle([x + 118, y + 6, x + 168, y + 18], fill=RED)
    elif kind == "scales":
        d.rectangle([x, y, x + w, y + h], fill=(232, 226, 212))
        d.line([(x + w // 2, y + 8), (x + w // 2, y + h - 10)], fill=INK,
               width=3)
        d.line([(x + 34, y + 16), (x + w - 34, y + 16)], fill=INK, width=3)
        for ex in (34, w - 34):
            d.line([(x + ex, y + 16), (x + ex, y + 30)], fill=INK, width=2)
            d.polygon([(x + ex - 14, y + 30), (x + ex + 14, y + 30),
                       (x + ex, y + 44)], fill=(120, 120, 116))
        d.rectangle([x + w // 2 - 22, y + h - 12, x + w // 2 + 22, y + h - 6],
                    fill=INK)
    elif kind == "sp500":
        d.rectangle([x, y, x + w, y + h], fill=(22, 35, 63))
        pts = [(x + 12, y + 12), (x + 52, y + 20), (x + 92, y + 16),
               (x + 132, y + 32), (x + 172, y + 40)]
        d.line(pts, fill=(255, 90, 80), width=3)
        d.text((x + 128, y + 6), "−2%", font=SANS_B(12), fill=(255, 90, 80))
    elif kind == "fire":
        d.rectangle([x, y, x + w, y + h], fill=(250, 220, 170))
        for fx, fh in [(40, 30), (90, 38), (140, 28)]:
            d.polygon([(x + fx - 12, y + h - 8), (x + fx, y + h - 8 - fh),
                       (x + fx + 12, y + h - 8)], fill=(230, 90, 30))
            d.polygon([(x + fx - 6, y + h - 8), (x + fx, y + h - 8 - fh + 12),
                       (x + fx + 6, y + h - 8)], fill=(255, 190, 60))
        d.rectangle([x, y + h - 8, x + w, y + h], fill=(90, 60, 40))

# ------------------------------------------------------------------ layout

def fit_font(draw, text, sizes, width, name="DejaVuSans.ttf"):
    """Largest font size from sizes (desc) that fits text in width."""
    for s in sizes:
        f = F(name, s)
        if draw.textlength(text, font=f) <= width:
            return f
    return F(name, sizes[-1])


def draw_region_bar(d):
    y, h = 130, 20
    seg = CW / len(REGIONS)
    x = M
    for name, count, color in REGIONS:
        d.rectangle([x, y, x + seg - 1, y + h], fill=color)
        label = "%s %d" % (name, count)
        f = SANS_B(9)
        tw = d.textlength(label, font=f)
        d.text((x + (seg - tw) / 2, y + 4), label, font=f, fill=WHITE)
        x += seg


def draw_stats(d):
    y, h = 156, 54
    cell = CW / len(STATS)
    for i, (num, label) in enumerate(STATS):
        x = M + i * cell
        if i:
            d.line([(x, y + 4), (x, y + h - 4)], fill=FAINT, width=1)
        nf = SERIF_B(25)
        d.text((x + 8, y + 2), num, font=nf, fill=RED)
        lines = wrap(d, label, SANS(9), cell - 16)
        text_block(d, x + 8, y + 32, lines[:2], SANS(9), MUTED, 11)


def draw_hero(d, hero, x, y, w, h, art):
    title, kicker, tag, headline, deck, _, _, _ = hero
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    art(d, x + 1, y + 1, w - 2, 112)
    label = title.split(":")[0]
    lf = SANS_B(13)
    lw = d.textlength(label, font=lf) + 14
    d.rectangle([x + 1, y + 1, x + 1 + lw, y + 22], fill=RED)
    d.text((x + 8, y + 4), label, font=lf, fill=WHITE)
    ky = y + 120
    d.text((x + 8, ky), kicker, font=SANS_B(9), fill=RED)
    tf = SANS_B(8)
    tw = d.textlength(tag, font=tf)
    d.text((x + w - 8 - tw, ky), tag, font=tf, fill=MUTED)
    lines = wrap(d, headline, SERIF_B(15), w - 16)
    hy = text_block(d, x + 8, ky + 17, lines[:2], SERIF_B(15), INK, 19)
    dlines = wrap(d, deck, SANS(10), w - 16)
    text_block(d, x + 8, hy + 3, dlines[:3], SANS(10), INK, 13)


def draw_mid(d, mid, x, y, w, h):
    kicker, tag, headline, deck, _, _, _, kind = mid
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    mid_art(d, kind, x + 1, y + 1, w - 2, 50)
    tf = SANS_B(7)
    tw = d.textlength(tag, font=tf)
    d.rectangle([x + w - 6 - tw, y + 4, x + w - 2, y + 17], fill=WHITE)
    d.text((x + w - 4 - tw, y + 5), tag, font=tf, fill=RED)
    ky = y + 56
    d.text((x + 6, ky), kicker, font=SANS_B(8), fill=RED)
    lines = wrap(d, headline, SANS_B(10), w - 12)
    hy = text_block(d, x + 6, ky + 13, lines[:2], SANS_B(10), INK, 12)
    dlines = wrap(d, deck, SANS(9), w - 12)
    text_block(d, x + 6, hy + 2, dlines[:2], SANS(9), INK, 11)


def draw_map(d):
    hy = 698
    d.text((M, hy), "WHERE IT HAPPENED", font=SANS_B(11), fill=INK)
    note = "● = story location · numbers match the list"
    nf = SANS(9)
    d.text((M + CW - d.textlength(note, font=nf), hy + 1), note, font=nf,
           fill=MUTED)
    mx, my, mw, mh = M, 716, CW, 124
    d.rectangle([mx, my, mx + mw, my + mh], fill=NAVY)
    for poly in LAND:
        pts = [project(lon, lat, mx, my, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=MAPLAND)
    for lon, lat, name in [(-100, 52, "NORTH AMERICA"), (-60, -14, "SOUTH AMERICA"),
                           (-25, 50, "EUROPE"), (5, -15, "AFRICA"),
                           (92, 48, "ASIA"), (140, -26, "OCEANIA")]:
        px, py = project(lon, lat, mx, my, mw, mh)
        d.text((px - 30, py - 5), name, font=SANS_B(8), fill=MAPLBL)
    stories = [(i + 1, h[5], h[6]) for i, h in enumerate(HEROES)]
    stories += [(i + 4, m[4], m[5]) for i, m in enumerate(MIDS)]
    stories += [(b[0], b[4], b[5]) for b in BRIEFS]
    for num, lat, lon in stories:
        px, py = project(lon, lat, mx, my, mw, mh)
        dx, dy = PIN_OFF.get(num, (0, 0))
        bx, by = px + dx, py + dy
        if (dx, dy) != (0, 0):
            d.line([(px, py), (bx, by)], fill=WHITE, width=1)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=WHITE)
        d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=RED,
                  outline=WHITE, width=1)
        s = str(num)
        sf = SANS_B(8)
        sw = d.textlength(s, font=sf)
        d.text((bx - sw / 2, by - 5), s, font=sf, fill=WHITE)
    d.text((mx + 6, my + mh - 14), "1–13 drawn · 14–36 briefs",
           font=SANS(8), fill=MAPLBL)


def draw_briefs(d):
    hy = 846
    d.text((M, hy), "ALSO ON FRIDAY 20 NOVEMBER — 23 MORE STORIES",
           font=SANS_B(11), fill=RED)
    cols = [BRIEFS[i:i + 8] for i in (0, 8, 16)]
    for ci, col in enumerate(cols):
        cx = M + ci * 327
        y = 866
        for num, loc, text, src, _, _, _ in col:
            line = "%d %s — %s (%s)" % (num, loc, text, src)
            f = fit_font(d, line, [8.5, 8], 314)
            d.text((cx, y), line, font=f, fill=INK)
            y += 11


def draw_datecheck(d):
    y, h = 958, 40
    d.rectangle([M, y, M + CW, y + h], outline=RED, width=2)
    head = "DATE CHECK  "
    hf = SANS_B(10)
    body = ("Left out as Thursday 19 November’s news: the Trump–Xi–Putin "
            "summit and peace declaration in Shenzhen · the ICJ’s Myanmar "
            "Rohingya genocide verdict · Anthropic’s $83 IPO pricing and "
            "Nasdaq debut · GTA VI’s midnight launch · the $190.4m Van "
            "Gogh sale. Not yet: BepiColombo’s Mercury orbit entry (Sat 21).")
    lines = wrap(d, body, SANS(10), CW - 16 - d.textlength(head, font=hf))
    d.text((M + 8, y + 5), head, font=hf, fill=RED)
    hx = M + 8 + d.textlength(head, font=hf)
    text_block(d, hx, y + 5, lines[:2], SANS(10), INK, 13)


def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # kicker
    d.text((M, 12), "THE WORLD IN ONE DAY", font=SANS_B(10), fill=RED)
    right = "36 STORIES · 7 REGIONS · EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
    rf = SANS_B(9)
    d.text((M + CW - d.textlength(right, font=rf), 13), right, font=rf,
           fill=INK)
    d.line([(M, 30), (M + CW, 30)], fill=INK, width=2)
    # masthead
    title = "Friday 20 November 2026"
    tf = SERIF_B(58)
    d.text(((W - d.textlength(title, font=tf)) / 2, 34), title, font=tf,
           fill=INK)
    sub = ("Russian missiles hit Kyiv’s bridges · Cyclone Akvan strikes "
           "India · An AI sell-off sinks Asia’s markets · UK and EU seal a deal")
    sf = SERIF(13)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 102), sub, font=sf,
           fill=MUTED)
    d.line([(M, 124), (M + CW, 124)], fill=INK, width=1)
    draw_region_bar(d)
    draw_stats(d)
    d.line([(M, 216), (M + CW, 216)], fill=INK, width=1)
    # heroes
    arts = [hero_kyiv, hero_akvan, hero_cop31]
    for i, hero in enumerate(HEROES):
        draw_hero(d, hero, M + i * 327, 222, 314, 214, arts[i])
    # mids: two rows of five
    for i, mid in enumerate(MIDS):
        row, col = divmod(i, 5)
        draw_mid(d, mid, M + col * 196, 442 + row * 128, 186, 122)
    draw_map(d)
    draw_briefs(d)
    draw_datecheck(d)
    foot = ("Every story here happened, or was first reported, on Friday "
            "20 November 2026. All times UTC. Sources named beside each "
            "story · Original drawings.")
    ff = SANS(8)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 1004), foot, font=ff,
           fill=MUTED)
    return img


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    draw_page().save(out, "PNG")
    print("wrote", out)
