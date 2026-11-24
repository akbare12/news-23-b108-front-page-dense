#!/usr/bin/env python3
"""news-23 b108 front-page-dense: draw entry.png (1024x1024) with PIL."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (247, 243, 232)
INK = (20, 20, 20)
BLACK = (12, 12, 12)
RED = (164, 30, 34)
DARKRED = (140, 22, 26)
NAVY = (16, 32, 64)
DARKGREEN = (18, 74, 52)
GOLD = (201, 162, 39)
GOLDLT = (232, 196, 90)
GRAY = (110, 108, 100)
LGRAY = (210, 206, 196)
GREEN = (168, 200, 150)
WHITE = (255, 255, 255)

FD = "/usr/share/fonts/truetype/dejavu/"
def fb(s): return ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", s)
def fr(s): return ImageFont.truetype(FD + "DejaVuSans.ttf", s)
def fsb(s): return ImageFont.truetype(FD + "DejaVuSerif-Bold.ttf", s)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

def wrap(text, font, maxw):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def ctext(x, y, s, font, fill, anchor="la"):
    d.text((x, y), s, font=font, fill=fill, anchor=anchor)

# ---------- masthead ----------
d.rectangle([0, 0, W, 56], fill=BLACK)
ctext(12, 6, "THE WORLD TODAY", fsb(42), WHITE)
ctext(W - 12, 20, "MONDAY 23 NOVEMBER 2026", fb(15), GOLD, anchor="ra")

# ---------- kicker ----------
d.rectangle([0, 56, W, 76], fill=RED)
ctext(W // 2, 61, "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
      fb(13), WHITE, anchor="ma")

# ---------- number strip: 2 rows x 5 ----------
nums = [
    ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", NAVY),
    ("11,762", "EBOLA CASES, DRC", (20, 90, 60)), ("10T won", "SEOUL STABILISATION FUND", (150, 110, 10)),
    ("2%", "BILLIONAIRE TAX IN PARIS", (20, 60, 110)),
    ("$450M", "SKUBAL DEAL", NAVY), ("165", "RUSSIAN MISSILES/WEEK", RED),
    ("12,000", "CLEARED IN MANCHESTER", (20, 90, 60)), ("264 kg", "EXPLOSIVES SEIZED", (150, 110, 10)),
    ("$107.3B", "ANTHROPIC IPO", NAVY),
]
cellw = W // 5
for i, (v, lab, col) in enumerate(nums):
    row, c = divmod(i, 5)
    x = c * cellw + 10
    y = 78 + row * 29
    ctext(x, y, v, fb(16), col)
    ctext(x, y + 17, lab, fr(8), INK)

# ---------- region bar ----------
regs = [("ASIA-PACIFIC 7", 7, (30, 70, 130)), ("AMERICAS 8", 8, RED),
        ("MIDDLE EAST 6", 6, (180, 140, 20)), ("EUROPE 5", 5, NAVY),
        ("AFRICA 3", 3, (40, 110, 60)), ("WORLD 2", 2, (110, 108, 100))]
x = 0
for name, n, col in regs:
    wseg = round(n / 31 * W)
    d.rectangle([x, 136, x + wseg - 1, 156], fill=col)
    ctext(x + wseg // 2, 141, name, fb(11), WHITE, anchor="ma")
    x += wseg

# ---------- UTC strip ----------
ctext(10, 159, "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
      fr(10), INK)
ctext(W - 10, 159, "~ APPROX", fr(10), GRAY, anchor="ra")

# ---------- hero scenes ----------
SX = [8, 348, 688]
SW = 328
SY, SH = 174, 146

# scene 1: Kospi skyline + falling chart
x0 = SX[0]
d.rectangle([x0, SY, x0 + SW, SY + SH], fill=NAVY)
# buildings with lit windows
import random
random.seed(108)
bx = x0 + 6
while bx < x0 + SW - 30:
    bw = random.randint(22, 40)
    bh = random.randint(55, 105)
    d.rectangle([bx, SY + SH - bh, bx + bw, SY + SH], fill=(24, 46, 88))
    for wy in range(SY + SH - bh + 8, SY + SH - 6, 12):
        for wx in range(bx + 4, bx + bw - 4, 9):
            if random.random() < 0.55:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 214, 90))
    bx += bw + 4
ctext(x0 + 10, SY + 6, "-3.3%", fb(34), WHITE)
pts = [(x0 + 12, SY + 62), (x0 + 60, SY + 66), (x0 + 108, SY + 60), (x0 + 156, SY + 74),
       (x0 + 204, SY + 82), (x0 + 252, SY + 96), (x0 + 316, SY + 118)]
d.line(pts, fill=(255, 140, 40), width=3)
for px, py in pts:
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=WHITE, outline=(255, 140, 40))
d.rectangle([x0, SY + SH - 16, x0 + SW, SY + SH], fill=BLACK)
ctext(x0 + 8, SY + SH - 14, "KOSPI 4,708.54  \u00b7  -161 PTS", fb(11), WHITE)

# scene 2: Guterres
x0 = SX[1]
d.rectangle([x0, SY, x0 + SW, SY + SH], fill=DARKGREEN)
ctext(x0 + 12, SY + 10, "150", fb(52), GOLD)
for i, ln in enumerate(["DELEGATES", "BACK A RISK", "FRAMEWORK"]):
    ctext(x0 + 12, SY + 62 + i * 22, ln, fb(20), GOLD)
# globe
cx, cy, r = x0 + SW - 58, SY + 62, 42
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(190, 225, 200), outline=(140, 190, 160), width=2)
d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(140, 190, 160), width=1)
d.line([cx - r, cy, cx + r, cy], fill=(140, 190, 160), width=1)
d.line([cx - r + 8, cy - r // 2, cx + r - 8, cy - r // 2], fill=(140, 190, 160), width=1)
d.line([cx - r + 8, cy + r // 2, cx + r - 8, cy + r // 2], fill=(140, 190, 160), width=1)
d.rectangle([x0, SY + SH - 16, x0 + SW, SY + SH], fill=BLACK)
ctext(x0 + 8, SY + SH - 14, "UN  \u00b7  BRIDGETOWN", fb(11), WHITE)

# scene 3: Power Index bars
x0 = SX[2]
d.rectangle([x0, SY, x0 + SW, SY + SH], fill=(240, 234, 220))
ctext(x0 + 10, SY + 6, "NARROWEST SINCE 2018", fb(11), INK)
ctext(x0 + SW - 10, SY + 6, "GAP 5.3", fb(11), RED, anchor="ra")
bars = [("US", 78.9, NAVY, 92), ("CHINA", 73.6, RED, 86), ("INDIA", 40.5, GOLD, 48)]
bx = x0 + 22
for name, val, col, bh in bars:
    d.rectangle([bx, SY + SH - 16 - bh, bx + 62, SY + SH - 16], fill=col)
    ctext(bx + 31, SY + SH - 16 - bh - 20, str(val), fb(15), INK, anchor="ma")
    ctext(bx + 31, SY + SH - 32, name, fb(11), WHITE, anchor="ma")
    bx += 96
d.rectangle([x0, SY + SH - 16, x0 + SW, SY + SH], fill=BLACK)
ctext(x0 + 8, SY + SH - 14, "ASIA POWER INDEX 2026", fb(11), WHITE)

# ---------- hero text ----------
heroes = [
    ("AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE"),
    ("GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS"),
    ("US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]
for i, (head, body, src) in enumerate(heroes):
    x0 = SX[i]
    hl = wrap(head, fb(20), SW)
    y = SY + SH + 6
    for ln in hl[:2]:
        ctext(x0, y, ln, fb(20), INK)
        y += 22
    bl = wrap(body, fr(11), SW)
    y += 2
    for ln in bl[:2]:
        ctext(x0, y, ln, fr(11), INK)
        y += 13
    sy = 408
    ctext(x0, sy, src, fr(9), GRAY)
    d.rectangle([x0 + SW - 62, sy - 1, x0 + SW, sy + 12], fill=(30, 70, 130))
    ctext(x0 + SW - 31, sy + 1, "REPORTED", fb(8), WHITE, anchor="ma")

# ---------- MORE OF THE DAY strip ----------
d.rectangle([0, 430, W, 452], fill=BLACK)
ctext(10, 436, "MORE OF THE DAY  \u2014  10 STORIES", fb(13), WHITE)

# ---------- cards ----------
cards = [
    ("AMERICAS", RED, "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED"),
    ("FBI", NAVY, "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", (20, 60, 110), "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", (20, 90, 60), "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", RED, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", RED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("LEGAL", NAVY, "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("TECH", (20, 60, 110), "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", (20, 90, 60), "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", (90, 40, 110), "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
cw, ch, gap = 198, 92, 7
for i, (cat, col, head, body, src, chip) in enumerate(cards):
    row, c = divmod(i, 5)
    x = 8 + c * (cw + gap)
    y = 458 + row * (ch + 6)
    d.rectangle([x, y, x + cw, y + ch], outline=LGRAY, width=1)
    d.rectangle([x, y, x + cw, y + 17], fill=col)
    ctext(x + 6, y + 3, cat, fb(10), WHITE)
    ctext(x + cw - 6, y + 3, str(i + 1), fb(10), WHITE, anchor="ra")
    hl = wrap(head, fb(11), cw - 12)
    yy = y + 21
    for ln in hl[:2]:
        ctext(x + 6, yy, ln, fb(11), INK)
        yy += 13
    ctext(x + 6, yy + 1, body, fr(10), INK)
    by = y + ch - 15
    ctext(x + 6, by, src, fr(8), GRAY)
    chipcol = (30, 70, 130) if chip == "REPORTED" else RED
    d.rectangle([x + cw - 62, by - 1, x + cw - 2, by + 11], fill=chipcol)
    ctext(x + cw - 33, by + 1, chip, fb(8), WHITE, anchor="ma")

# ---------- map + ALSO strips ----------
d.rectangle([0, 648, 330, 670], fill=BLACK)
ctext(10, 654, "WHERE IT HAPPENED", fb(13), WHITE)
d.rectangle([338, 648, W, 670], fill=BLACK)
ctext(348, 654, "ALSO ON MONDAY", fb(13), WHITE)

# simplified world blobs
d.polygon([(30, 700), (120, 680), (170, 710), (150, 790), (90, 830), (40, 780)], fill=GREEN)
d.polygon([(180, 700), (260, 690), (300, 730), (270, 800), (200, 790)], fill=GREEN)
d.polygon([(200, 850), (280, 840), (310, 880), (240, 900), (200, 880)], fill=GREEN)
pins = [(52, 716, "1"), (86, 812, "2"), (140, 700, "3"), (108, 756, "4"),
        (128, 742, "5"), (196, 716, "6"), (150, 758, "7"), (96, 736, "8"),
        (118, 782, "9"), (132, 800, "10"), (168, 700, "11"), (216, 700, "12"),
        (250, 726, "13")]
for px, py, n in pins:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
    ctext(px, py - 6, n, fb(9), WHITE, anchor="ma")
ctext(10, 880, "Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing", fr(9), INK)
ctext(10, 892, "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Chicago \u00b7 8 SF", fr(9), INK)
ctext(10, 904, "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow", fr(9), INK)

also = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: the day after Antalya pact rejected",
    "18. Israel unity talks resume",
    "19. Gaza: two killed in Israeli strike",
    "20. West Bank settler attacks",
    "21. Iran war: no deal in sight",
    "22. Lebanon seizes 264 kg explosives",
    "23. Bahrain: strike hits plant, 2 hurt",
    "24. Benghazi: UN demands probe  [CLAIM]",
    "25. Sudan: defences down drones  [CLAIM]",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row",
    "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
for i, item in enumerate(also):
    col = i % 2
    row = i // 2
    x = 348 + col * 340
    y = 678 + row * 26
    if "[CLAIM]" in item:
        base, _ = item.split("  [CLAIM]")
        ctext(x, y, base, fr(11), INK)
        ctext(x + d.textlength(base, font=fr(11)) + 4, y, "[CLAIM]", fb(10), RED)
    else:
        ctext(x, y, item, fr(11), INK)

# ---------- DATE CHECK ----------
d.rectangle([8, 922, W - 8, 972], outline=RED, width=2)
ctext(14, 926, "DATE CHECK", fb(12), RED)
ctext(W - 14, 926, "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", fb(9), RED, anchor="ra")
ctext(14, 942, "LEFT OUT \u2014 NOT 23 NOV:  Dems 258 seats (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo (22 Nov)  \u00b7  EU\u2013Indonesia (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar (19 Nov)",
      fr(10), INK)
ctext(14, 956, "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
      fr(10), INK)

# ---------- footer ----------
ctext(10, 978, "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).", fr(9), GRAY)
ctext(10, 990, "CHIPS: REPORTED = confirmed by wires. CLAIM = one side's claim, not independently confirmed. ONGOING = still developing.", fr(9), GRAY)
ctext(10, 1001, "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.", fr(9), GRAY)
ctext(W // 2, 1013, "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions", fb(10), GOLD, anchor="ma")

out = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"), "entry.png")
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
img.save(out, optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
