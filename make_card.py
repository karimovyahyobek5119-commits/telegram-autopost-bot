"""
make_card.py — Matnni "lol qiladigan" chiroyli kartochka (rasm)ga aylantiradi.
Hech qanday pullik API kerak emas — faqat Pillow (PIL) bilan ishlaydi.

Ishlatish (kod ichidan):
    from make_card import create_card
    create_card(
        text="Bilasizmi? ...",
        out_path="channels/faktura/images/001.png",
        theme="faktura",
        emoji="🌍",
    )

Yangi kartochka qo'shish uchun shu faylni o'zgartirish shart emas —
generate_batch.py orqali matnlarni ro'yxat qilib bering, u avtomatik chaqiradi.
"""

import textwrap
from PIL import Image, ImageDraw, ImageFont

SIZE = (1080, 1080)
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_EMOJI = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

# Har kanal uchun rang uslubi (gradient boshi -> oxiri, matn rangi)
THEMES = {
    "math_olimjon":     {"c1": (76, 29, 149),  "c2": (139, 92, 246),  "text": (255, 255, 255), "accent": (250, 204, 21)},
    "faktura":          {"c1": (6, 78, 59),    "c2": (16, 185, 129),  "text": (255, 255, 255), "accent": (250, 204, 21)},
    "matematika_milliy":{"c1": (30, 58, 138),  "c2": (59, 130, 246),  "text": (255, 255, 255), "accent": (251, 146, 60)},
    "fizika_milliy":    {"c1": (127, 29, 29),  "c2": (220, 38, 38),   "text": (255, 255, 255), "accent": (56, 189, 248)},
}


def _vertical_gradient(size, c1, c2):
    w, h = size
    img = Image.new("RGB", size, c1)
    draw = ImageDraw.Draw(img)
    for y in range(h):
        ratio = y / h
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img


def _wrap_text(text, font, max_width, draw):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = f"{current} {word}".strip()
        if draw.textlength(test, font=font) <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def create_card(text: str, out_path: str, theme: str, emoji: str = "✨", label: str = ""):
    style = THEMES[theme]
    img = _vertical_gradient(SIZE, style["c1"], style["c2"])
    draw = ImageDraw.Draw(img)

    margin = 90
    max_width = SIZE[0] - 2 * margin

    # Katta emoji tepada (rangli, Noto Color Emoji fonti orqali)
    try:
        emoji_font = ImageFont.truetype(FONT_EMOJI, 109)  # Noto Color Emoji fixed strike size
        bbox = draw.textbbox((0, 0), emoji, font=emoji_font, embedded_color=True)
        ew = bbox[2] - bbox[0]
        draw.text(((SIZE[0] - ew) / 2, 90), emoji, font=emoji_font, embedded_color=True)
    except Exception:
        pass  # emoji topilmasa, kartochka emojisiz ham chiroyli chiqadi

    # Asosiy matn — o'rtada, avtomatik hajm moslashtirish
    font_size = 64
    body_font = ImageFont.truetype(FONT_BOLD, font_size)
    lines = _wrap_text(text, body_font, max_width, draw)
    while len(lines) > 7 and font_size > 36:
        font_size -= 4
        body_font = ImageFont.truetype(FONT_BOLD, font_size)
        lines = _wrap_text(text, body_font, max_width, draw)

    line_height = int(font_size * 1.35)
    total_h = line_height * len(lines)
    start_y = (SIZE[1] - total_h) / 2 + 40

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=body_font)
        lw = bbox[2] - bbox[0]
        draw.text(((SIZE[0] - lw) / 2, start_y + i * line_height), line,
                   font=body_font, fill=style["text"])

    # Pastda kichik label (kanal nomi)
    if label:
        small_font = ImageFont.truetype(FONT_REGULAR, 30)
        bbox = draw.textbbox((0, 0), label, font=small_font)
        lw = bbox[2] - bbox[0]
        draw.text(((SIZE[0] - lw) / 2, SIZE[1] - 80), label,
                   font=small_font, fill=style["accent"])

    img.save(out_path, "PNG")
    return out_path
