from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).parent
SRC = ROOT.parents[2] / "docs" / "assets" / "product-preview.png"
OUT = ROOT / "assets"
OUT.mkdir(exist_ok=True)

font_path = Path(r"C:\Windows\Fonts\malgun.ttf")
bold_path = Path(r"C:\Windows\Fonts\malgunbd.ttf")
def font(size, bold=False):
    return ImageFont.truetype(str(bold_path if bold else font_path), size)

source = Image.open(SRC).convert("RGB")
# Crop deliberately excludes the stale ‘총 171개 게임’ header from this historical preview.
ui = source.crop((350, 100, 1350, 700)).resize((960, 576), Image.Resampling.LANCZOS)

def card(path, size, title, subtitle, accent):
    w, h = size
    im = Image.new("RGB", size, "#071526")
    d = ImageDraw.Draw(im)
    for y in range(h):
        v = int(16 + 20 * y / h)
        d.line((0, y, w, y), fill=(6, v, 39))
    landscape = w / h > 1.2
    if landscape:
        # Landscape channels need a smaller, fully contained preview below the copy.
        px = (w - int(w * 0.56)) // 2
        pw = w - px * 2
        py = int(h * 0.31)
        title_y = int(h * 0.145)
        title_font = font(max(32, w // 38), True)
        subtitle_y = int(h * 0.238)
        subtitle_font = font(max(18, w // 62))
        footer_y = int(h * 0.93)
    else:
        px = (w - int(w * 0.89)) // 2
        pw = w - px * 2
        py = int(h * 0.28)
        title_y = int(h * 0.145)
        title_font = font(max(36, w // 21), True)
        subtitle_y = title_y + int(h * 0.078)
        subtitle_font = font(max(20, w // 43))
        footer_y = h - int(h * 0.085)
    ph = int(pw * ui.height / ui.width)
    preview = ui.resize((pw, ph), Image.Resampling.LANCZOS)
    mask = Image.new("L", preview.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, pw - 1, ph - 1), radius=max(22, w // 45), fill=255)
    im.paste(preview, (px, py), mask)
    d.rounded_rectangle((px, py, px + pw, py + ph), radius=max(22, w // 45), outline=accent, width=max(3, w // 300))
    d.rounded_rectangle((px, int(h * 0.075), px + int(w * 0.28), int(h * 0.075) + int(h * 0.055)), radius=16, fill=accent)
    d.text((px + 18, int(h * 0.075) + 9), "JANGYOON'S GAME ARCADE", font=font(max(16, w // 55), True), fill="#071526")
    d.text((px, title_y), title, font=title_font, fill="#F4F8FF")
    d.text((px, subtitle_y), subtitle, font=subtitle_font, fill="#B9C9DD")
    footer = "모험 · 학습 · 창의 · 전통놀이  |  지금 게임 고르기"
    d.text((px, footer_y), footer, font=font(max(16, w // 55)), fill="#B9C9DD")
    im.save(path, optimize=True)

card(OUT / "instagram-card.png", (1080, 1350), "터치로 바로 즐기는", "어린이 미니게임 228개", "#55D7FF")
card(OUT / "threads-card.png", (1200, 675), "설치 없이 바로 여는 게임 놀이터", "228개 어린이 미니게임을 한 곳에", "#7CF2B0")
card(OUT / "x-card.png", (1600, 900), "어린이 미니게임 228개", "탭 · 스와이프 · 드래그로 골라 시작하기", "#FFD968")
