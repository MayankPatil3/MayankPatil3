from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1280, 340
MINT = (124, 255, 178)
VIOLET = (157, 140, 255)
TEXT = (232, 236, 241)
MUTED = (154, 166, 178)
DIM = (110, 122, 136)

BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
MONO = "/System/Library/Fonts/Menlo.ttc"

def font(path, size, index=0):
    return ImageFont.truetype(path, size, index=index)

img = Image.new("RGB", (W, H), (10, 11, 13))
draw = ImageDraw.Draw(img)

# vertical gradient
top = (9, 10, 12)
bot = (15, 18, 23)
for y in range(H):
    t = y / (H - 1)
    draw.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))

# glows
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([-260, -300, 480, 260], fill=(*MINT, 38))
gd.ellipse([900, 150, 1520, 620], fill=(*VIOLET, 34))
glow = glow.filter(ImageFilter.GaussianBlur(110))
img = Image.alpha_composite(img.convert("RGBA"), glow)

# faint grid
grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gr = ImageDraw.Draw(grid)
for x in range(0, W, 40):
    gr.line([(x, 0), (x, H)], fill=(255, 255, 255, 7))
for y in range(0, H, 40):
    gr.line([(0, y), (W, y)], fill=(255, 255, 255, 7))
img = Image.alpha_composite(img, grid)

draw = ImageDraw.Draw(img, "RGBA")

# isometric cube field, right side
def cube(cx, cy, s, color, alpha):
    h = s * 0.866
    top_p = [(cx, cy - s), (cx + h, cy - s / 2), (cx, cy), (cx - h, cy - s / 2)]
    left_p = [(cx - h, cy - s / 2), (cx, cy), (cx, cy + s), (cx - h, cy + s / 2)]
    right_p = [(cx + h, cy - s / 2), (cx, cy), (cx, cy + s), (cx + h, cy + s / 2)]
    for poly in (top_p, left_p, right_p):
        draw.polygon(poly, outline=(*color, alpha))

for (cx, cy, s, col, a) in [
    (1040, 150, 62, MINT, 70),
    (1160, 205, 44, MINT, 45),
    (960, 230, 34, VIOLET, 55),
    (1120, 90, 24, VIOLET, 40),
]:
    cube(cx, cy, s, col, a)

# logo diamond
lx, ly, ls = 92, 118, 26
draw.polygon([(lx, ly - ls), (lx + ls, ly), (lx, ly + ls), (lx - ls, ly)],
             outline=(*MINT, 235), width=4)
draw.rectangle([lx - 3, ly - 3, lx + 3, ly + 3], fill=(*MINT, 235))

name_f = font(BOLD, 70)
tag_f = font(REG, 25)
chip_f = font(MONO, 16, index=0)
draw.text((138, 70), "Mayank", font=name_f, fill=TEXT)
draw.text((141, 154), "Building performance tooling for Minecraft servers.", font=tag_f, fill=(211, 219, 228))

# chips
chips = ["Java 21", "Paper 1.21", "SQLite / MySQL", "19 tests"]
cx = 141
cy = 222
pad_x, pad_y = 15, 8
for label in chips:
    bbox = draw.textbbox((0, 0), label, font=chip_f)
    w = bbox[2] - bbox[0] + pad_x * 2
    h = bbox[3] - bbox[1] + pad_y * 2 + 4
    draw.rounded_rectangle([cx, cy, cx + w, cy + h], radius=7,
                           outline=(255, 255, 255, 38), width=1,
                           fill=(255, 255, 255, 6))
    draw.text((cx + pad_x, cy + pad_y + 1), label, font=chip_f, fill=(174, 185, 198))
    cx += w + 10

# bottom hairline accent
draw.rectangle([0, H - 3, W, H - 1], fill=(*MINT, 70))

OUT = Path(__file__).with_name("banner.png")
img.convert("RGB").save(OUT, optimize=True)
print("saved", OUT, img.size)
