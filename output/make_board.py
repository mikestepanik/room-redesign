#!/usr/bin/env python3
"""Render an interior-designer style presentation board as a PNG."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W, H = 1800, 2700
BG = (22, 24, 30)
INK = (232, 221, 208)
DIM = (160, 150, 138)
GOLD = (201, 169, 97)
LINE = (60, 58, 55)
PANEL = (30, 33, 40)

PALETTE = [
    ("Deep Navy",        "#1A2238", "Walls (3 sides)"),
    ("Fluted Black Oak", "#1F1A15", "Accent wall behind desk"),
    ("Warm White",       "#F2EBDD", "Smooth ceiling"),
    ("White Oak",        "#C4A57C", "Floor planks"),
    ("Forest Linen",     "#2A3B2C", "Duvet"),
    ("Cream Waffle",     "#E8DDC8", "Throw / pillows"),
    ("Brushed Brass",    "#B5895A", "Hardware / lamp"),
    ("Amber Underglow",  "#D4983F", "PC + bias light"),
]

def font(size, bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---------- HEADER ----------
d.rectangle([0, 0, W, 200], fill=PANEL)
d.line([(80, 195), (W - 80, 195)], fill=GOLD, width=2)
d.text((80, 50),  "BEDROOM REDESIGN", font=font(56, bold=True), fill=INK)
d.text((80, 115), "The Modern Gamer's Sanctuary  ·  Presentation Board 01",
       font=font(28), fill=DIM)
d.text((W - 80, 60), "01 / 01", font=font(28, bold=True), fill=GOLD, anchor="ra")
d.text((W - 80, 100), "Scale: NTS", font=font(22), fill=DIM, anchor="ra")
d.text((W - 80, 135), "Issued for review", font=font(22), fill=DIM, anchor="ra")

# ---------- SECTION: CONCEPT ----------
y = 240
d.text((80, y), "01  CONCEPT", font=font(22, bold=True), fill=GOLD)
d.text((80, y + 36), "Moody masculine sanctuary built around the gaming workstation.",
       font=font(30, bold=True), fill=INK)
concept_lines = [
    "Keep what works: the deep wall color, the dedicated PC battle station, the cozy enclosure.",
    "Fix what doesn't: clutter, exposed cables, mismatched curtains, patchy paint, popcorn ceiling.",
    "Replace gamer-RGB with one warm amber underglow + 2700K bias light. Hide every cable.",
]
for i, line in enumerate(concept_lines):
    d.text((80, y + 90 + i * 36), "·  " + line, font=font(22), fill=INK)

# ---------- SECTION: PALETTE ----------
y = 470
d.text((80, y), "02  COLOR + MATERIAL PALETTE", font=font(22, bold=True), fill=GOLD)
sw_w, sw_h, gap = 195, 240, 12
sx = 80
for i, (name, hx, role) in enumerate(PALETTE):
    x0 = sx + i * (sw_w + gap)
    y0 = y + 60
    d.rectangle([x0, y0, x0 + sw_w, y0 + sw_h], fill=hex_to_rgb(hx))
    d.text((x0, y0 + sw_h + 14), name, font=font(20, bold=True), fill=INK)
    d.text((x0, y0 + sw_h + 42), hx, font=font(18), fill=GOLD)
    # role wrapped
    role_lines = role.split(" / ")
    for j, rl in enumerate(role_lines):
        d.text((x0, y0 + sw_h + 70 + j * 24), rl, font=font(17), fill=DIM)

# ---------- SECTION: FLOOR PLAN ----------
y = 1080
d.text((80, y), "03  FLOOR PLAN  ·  view from doorway",
       font=font(22, bold=True), fill=GOLD)
plan_x0, plan_y0 = 80, y + 70
plan_w, plan_h = 1100, 800
# room outline
d.rectangle([plan_x0, plan_y0, plan_x0 + plan_w, plan_y0 + plan_h],
            outline=INK, width=3)

# helper rect with label
def piece(x, y, w, h, label, fill, txtcolor=INK):
    d.rectangle([x, y, x + w, y + h], fill=fill, outline=GOLD, width=2)
    d.text((x + 12, y + 10), label, font=font(18, bold=True), fill=txtcolor)

# DESK (back wall - top of plan)
piece(plan_x0 + 60, plan_y0 + 30, plan_w - 120, 130,
      "BUILT-IN DESK  +  ULTRAWIDE  +  VERTICAL  +  PC TOWER", hex_to_rgb("#1F1A15"))
# acoustic panels behind desk - shown as inset stripe
for k in range(8):
    bx = plan_x0 + 80 + k * 125
    d.rectangle([bx, plan_y0 + 22, bx + 100, plan_y0 + 28], fill=hex_to_rgb("#3A3A40"))
# chair
d.ellipse([plan_x0 + plan_w/2 - 60, plan_y0 + 200,
           plan_x0 + plan_w/2 + 60, plan_y0 + 310], outline=INK, width=2,
           fill=(40, 42, 48))
d.text((plan_x0 + plan_w/2, plan_y0 + 250), "CHAIR",
       font=font(18, bold=True), fill=INK, anchor="mm")

# BED (right wall) - bed extends in from right
bed_w, bed_h = 380, 520
bx = plan_x0 + plan_w - bed_w - 20
by = plan_y0 + 240
piece(bx, by, bed_w, bed_h, "QUEEN PLATFORM BED", hex_to_rgb("#2A3B2C"))
# pillows
d.rectangle([bx + 20, by + 20, bx + bed_w - 20, by + 90],
            fill=hex_to_rgb("#E8DDC8"), outline=GOLD, width=1)
d.text((bx + bed_w/2, by + 55), "pillows",
       font=font(16), fill=(60, 50, 40), anchor="mm")
# nightshelf above
d.rectangle([bx + 30, by - 30, bx + bed_w - 30, by - 8],
            fill=hex_to_rgb("#3A2E22"), outline=GOLD, width=1)
d.text((bx + bed_w/2, by - 19), "floating walnut shelf  ·  arc lamp  ·  monstera",
       font=font(13), fill=INK, anchor="mm")

# CREDENZA + WINDOW (left wall)
cred_w, cred_h = 90, 360
piece(plan_x0 + 20, plan_y0 + 260, cred_w, cred_h,
      "", hex_to_rgb("#3A2E22"))
d.text((plan_x0 + 20 + cred_w/2, plan_y0 + 260 + cred_h/2),
       "WALNUT\nCREDENZA",
       font=font(15, bold=True), fill=INK, anchor="mm", align="center")
# window over credenza shown as gap in wall
d.line([(plan_x0, plan_y0 + 280), (plan_x0, plan_y0 + 540)],
       fill=hex_to_rgb("#E8DDC8"), width=8)
d.text((plan_x0 - 8, plan_y0 + 410), "WINDOW",
       font=font(15, bold=True), fill=GOLD, anchor="rm")
d.text((plan_x0 - 8, plan_y0 + 438), "linen drape + blackout shade",
       font=font(13), fill=DIM, anchor="rm")

# RUG under bed/center
d.rectangle([plan_x0 + 200, plan_y0 + 380, plan_x0 + 760, plan_y0 + 720],
            outline=GOLD, width=1)
d.text((plan_x0 + 480, plan_y0 + 550), "charcoal wool area rug",
       font=font(16), fill=DIM, anchor="mm")

# SHOE CABINET + VR shelf (lower left, near door)
piece(plan_x0 + 20, plan_y0 + 640, 110, 130, "SHOE\nCABINET", hex_to_rgb("#3A2E22"))
d.text((plan_x0 + 150, plan_y0 + 660), "VR shelf  ·  brass wall valet",
       font=font(15), fill=INK)

# DOOR (lower left)
d.arc([plan_x0 - 4, plan_y0 + plan_h - 200, plan_x0 + 200, plan_y0 + plan_h + 4],
      start=270, end=360, fill=GOLD, width=3)
d.text((plan_x0 + 30, plan_y0 + plan_h - 50), "DOOR",
       font=font(16, bold=True), fill=GOLD)

# Compass / view indicator
d.text((plan_x0 + plan_w - 130, plan_y0 + plan_h + 16),
       "↑ camera POV", font=font(16), fill=DIM)

# ---------- SIDEBAR: KEY PIECES ----------
sb_x = 1230
sb_y = 1150
d.text((sb_x, sb_y - 4), "04  KEY PIECES", font=font(22, bold=True), fill=GOLD)
pieces = [
    ("Bed",       "Low matte-black-oak platform, queen, upholstered charcoal headboard"),
    ("Bedding",   "Washed linen duvet (forest), cream waffle throw, white euro shams,\nolive lumbar cushion"),
    ("Desk",      "Wall-to-wall built-in, matte black oak, integrated cable channels"),
    ("Monitor",   "34\" ultrawide curved (primary) + 24\" portrait (secondary)"),
    ("Chair",     "Herman Miller Aeron, graphite mesh  ·  ergonomic over gaming"),
    ("Lighting",  "2700K bias LED behind monitors  ·  matte black arc floor lamp\nover desk  ·  brass pendant over credenza  ·  cove perimeter"),
    ("Window",    "Floor-to-ceiling oatmeal linen drapes + smart blackout roller"),
    ("Credenza",  "Slat-front walnut, brushed brass pulls, replaces the dresser"),
    ("Floor",     "Wide-plank European white oak satin, charcoal wool rug under bed"),
    ("Walls",     "Three walls deep navy matte  ·  back wall fluted black oak slats"),
    ("Ceiling",   "Skim-coated smooth, warm white  ·  no popcorn"),
    ("Cables",    "Every wire in-wall or in raceway  ·  zero visible runs"),
]
yy = sb_y + 50
for label, body in pieces:
    d.text((sb_x, yy), label, font=font(19, bold=True), fill=INK)
    for li, ln in enumerate(body.split("\n")):
        d.text((sb_x + 130, yy + li * 24), ln, font=font(17), fill=DIM)
    yy += 24 * len(body.split("\n")) + 18

# ---------- LIGHTING PLAN ----------
y = 1980
d.text((80, y), "05  LIGHTING PLAN  ·  three zones, all 2700K",
       font=font(22, bold=True), fill=GOLD)
zones = [
    ("AMBIENT", "Cove perimeter LED at ceiling edge, dimmable. Sets the room mood."),
    ("TASK",    "Arc floor lamp over desk + monitor bias light strip. For work."),
    ("ACCENT",  "Brass pendant over credenza, nightshelf reading lamp, PC underglow."),
]
for i, (zname, zdesc) in enumerate(zones):
    zx = 80 + i * 580
    d.rectangle([zx, y + 60, zx + 530, y + 230], outline=GOLD, width=2)
    d.text((zx + 20, y + 78), zname, font=font(28, bold=True), fill=GOLD)
    # wrap description
    words = zdesc.split()
    line, lines = "", []
    for w in words:
        test = (line + " " + w).strip()
        if d.textlength(test, font=font(20)) > 480:
            lines.append(line); line = w
        else:
            line = test
    if line: lines.append(line)
    for j, ln in enumerate(lines):
        d.text((zx + 20, y + 130 + j * 30), ln, font=font(20), fill=INK)

# ---------- DESIGN MOVES TABLE ----------
y = 2280
d.text((80, y), "06  KEY DESIGN MOVES  ·  before → after",
       font=font(22, bold=True), fill=GOLD)
moves = [
    ("Patchy navy walls",        "Smooth matte navy + fluted black-oak accent wall"),
    ("Popcorn ceiling",          "Skim-coated smooth, warm white"),
    ("Cables along wall/ceiling","All cables hidden in raceways or in-wall"),
    ("Mismatched curtains",      "Linen drapes + blackout roller shade"),
    ("Cluttered dresser top",    "Curated walnut credenza, three-object styling"),
    ("Rainbow RGB PC + chair",   "Single warm amber underglow, mesh ergonomic chair"),
    ("Plaid bedding",            "Forest linen duvet + cream waffle throw"),
    ("Open shoe pile",           "Tall walnut shoe cabinet + wall valet"),
]
col_y = y + 60
for i, (b, a) in enumerate(moves):
    row_y = col_y + i * 42
    d.text((100, row_y), "✕", font=font(22, bold=True), fill=(180, 90, 90))
    d.text((140, row_y), b, font=font(20), fill=DIM)
    d.text((860, row_y), "→", font=font(22, bold=True), fill=GOLD)
    d.text((910, row_y), a, font=font(20), fill=INK)

# ---------- FOOTER ----------
d.line([(80, H - 70), (W - 80, H - 70)], fill=LINE, width=1)
d.text((80, H - 50), "Banana Claude  ·  Creative Director deliverable",
       font=font(18), fill=DIM)
d.text((W - 80, H - 50), "Issued 2026-05-19",
       font=font(18), fill=DIM, anchor="ra")

out = "/home/user/room-redesign/output/redesign_board.png"
img.save(out, "PNG", optimize=True)
print(out)
