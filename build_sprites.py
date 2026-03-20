#!/usr/bin/env python3
"""Build sprite sheet from original character images for Pyxel.

Usage: python3 build_sprites.py
Input:  assets/originals/{poemu,bagumaru,hattari,nabiko}.png (1024x1024 RGBA)
Output: assets/sprites.png (256x96, 4 chars @ 64x64 + nabiko 32x32 icon)
"""

import os
from PIL import Image

# Pyxel default 16-color palette (RGB)
PYXEL_PALETTE = [
    (0, 0, 0),        # 0: black
    (43, 51, 95),      # 1: navy
    (126, 32, 114),    # 2: purple
    (25, 149, 44),     # 3: dark green
    (139, 72, 82),     # 4: brown
    (57, 92, 152),     # 5: dark blue-gray
    (169, 193, 255),   # 6: light lavender
    (238, 238, 238),   # 7: white
    (212, 24, 108),    # 8: red/magenta
    (211, 132, 65),    # 9: orange
    (233, 195, 91),    # 10: yellow
    (112, 198, 169),   # 11: green/teal
    (118, 150, 222),   # 12: sky blue
    (163, 163, 163),   # 13: gray
    (255, 151, 152),   # 14: pink
    (237, 199, 176),   # 15: peach
]

COLKEY = 0  # C_BLACK - used as transparent color in Pyxel

# Character files in sprite sheet order (left to right)
CHARACTERS = [
    "poemu.png",      # slot 0: (0,0)
    "bagumaru.png",   # slot 1: (64,0)
    "hattari.png",    # slot 2: (128,0)
    "nabiko.png",     # slot 3: (192,0)
]

SPRITE_SIZE = 64
WATERMARK_CROP = 60  # pixels to crop from bottom-right for Gemini mark

# Background/logo processing for image bank 1
BG_FILENAMES = ["bg_stage1.png", "bg_stage2.png", "bg_stage3.png",
                "bg_stage4.png", "bg_stage5.png"]
BG_SIZE = (90, 80)   # stored size; drawn at 3x = 270x240
BG_POSITIONS = [(0, 0), (90, 0), (0, 80), (90, 80), (0, 160)]
LOGO_FILENAME = "title_logo.png"
LOGO_WIDTH = 135      # stored width; drawn at 2x = 270
LOGO_HEIGHT = 72      # stored height; drawn at 2x = 144
LOGO_POS = (0, 0)     # position in bg sprite sheet (bg stages unused now)


def color_distance(c1, c2):
    """Weighted Euclidean distance (human perception weighting)."""
    dr = c1[0] - c2[0]
    dg = c1[1] - c2[1]
    db = c1[2] - c2[2]
    return (dr * dr * 2) + (dg * dg * 4) + (db * db * 3)


def nearest_palette_color(r, g, b):
    """Find nearest Pyxel palette color index, excluding COLKEY."""
    best_idx = 0
    best_dist = float("inf")
    for i, (pr, pg, pb) in enumerate(PYXEL_PALETTE):
        if i == COLKEY:
            continue  # skip colkey color
        d = color_distance((r, g, b), (pr, pg, pb))
        if d < best_dist:
            best_dist = d
            best_idx = i
    return best_idx


def find_character_bbox(img):
    """Find bounding box of non-transparent pixels."""
    w, h = img.size
    pixels = img.load()
    min_x, min_y = w, h
    max_x, max_y = 0, 0

    for y in range(h):
        for x in range(w):
            a = pixels[x, y][3]
            if a > 30:  # threshold for "visible"
                r, g, b = pixels[x, y][:3]
                # Also skip near-black background pixels
                if r + g + b > 15:
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)

    if max_x <= min_x or max_y <= min_y:
        return (0, 0, w, h)

    # Add small padding
    pad = 4
    min_x = max(0, min_x - pad)
    min_y = max(0, min_y - pad)
    max_x = min(w, max_x + pad)
    max_y = min(h, max_y + pad)

    return (min_x, min_y, max_x, max_y)


def process_character(filepath):
    """Process a single character image into a 64x64 Pyxel-palette sprite."""
    img = Image.open(filepath).convert("RGBA")
    w, h = img.size

    # Step 1: Crop out Gemini watermark (bottom-right)
    crop_w = w - WATERMARK_CROP
    crop_h = h - WATERMARK_CROP
    img = img.crop((0, 0, crop_w, crop_h))

    # Step 2: Find character bounding box
    bbox = find_character_bbox(img)
    char_img = img.crop(bbox)

    # Step 3: Make it square (pad shorter side)
    cw, ch = char_img.size
    max_dim = max(cw, ch)
    square = Image.new("RGBA", (max_dim, max_dim), (0, 0, 0, 0))
    offset_x = (max_dim - cw) // 2
    offset_y = (max_dim - ch) // 2
    square.paste(char_img, (offset_x, offset_y))

    # Step 4: Resize to 64x64 with high-quality downsampling
    resized = square.resize((SPRITE_SIZE, SPRITE_SIZE), Image.LANCZOS)

    # Step 5: Map to Pyxel palette
    result = Image.new("RGB", (SPRITE_SIZE, SPRITE_SIZE))
    src_pixels = resized.load()
    dst_pixels = result.load()

    for y in range(SPRITE_SIZE):
        for x in range(SPRITE_SIZE):
            r, g, b, a = src_pixels[x, y]
            if a < 80 or (r + g + b < 50):
                # Transparent or near-black background → colkey color
                dst_pixels[x, y] = PYXEL_PALETTE[COLKEY]
            else:
                # Map to nearest palette color
                idx = nearest_palette_color(r, g, b)
                dst_pixels[x, y] = PYXEL_PALETTE[idx]

    return result


def process_character_small(filepath, size=32):
    """Process a character image into a small icon (e.g. 32x32)."""
    img = Image.open(filepath).convert("RGBA")
    w, h = img.size

    crop_w = w - WATERMARK_CROP
    crop_h = h - WATERMARK_CROP
    img = img.crop((0, 0, crop_w, crop_h))

    bbox = find_character_bbox(img)
    char_img = img.crop(bbox)

    cw, ch = char_img.size
    max_dim = max(cw, ch)
    square = Image.new("RGBA", (max_dim, max_dim), (0, 0, 0, 0))
    offset_x = (max_dim - cw) // 2
    offset_y = (max_dim - ch) // 2
    square.paste(char_img, (offset_x, offset_y))

    resized = square.resize((size, size), Image.LANCZOS)

    result = Image.new("RGB", (size, size))
    src_pixels = resized.load()
    dst_pixels = result.load()

    for y in range(size):
        for x in range(size):
            r, g, b, a = src_pixels[x, y]
            if a < 80 or (r + g + b < 50):
                dst_pixels[x, y] = PYXEL_PALETTE[COLKEY]
            else:
                idx = nearest_palette_color(r, g, b)
                dst_pixels[x, y] = PYXEL_PALETTE[idx]

    return result


def nearest_palette_color_full(r, g, b):
    """Find nearest Pyxel palette color including index 0 (black)."""
    best_idx = 0
    best_dist = float("inf")
    for i, (pr, pg, pb) in enumerate(PYXEL_PALETTE):
        d = color_distance((r, g, b), (pr, pg, pb))
        if d < best_dist:
            best_dist = d
            best_idx = i
    return best_idx


def process_background(filepath, target_size):
    """Process background: crop watermark, resize, 16-color (including black)."""
    img = Image.open(filepath).convert("RGBA")
    w, h = img.size
    img = img.crop((0, 0, w - WATERMARK_CROP, h - WATERMARK_CROP))
    img = img.resize(target_size, Image.LANCZOS)
    result = Image.new("RGB", target_size)
    src = img.load()
    dst = result.load()
    for y in range(target_size[1]):
        for x in range(target_size[0]):
            r, g, b, a = src[x, y]
            idx = nearest_palette_color_full(r, g, b)
            dst[x, y] = PYXEL_PALETTE[idx]
    return result


def process_logo(filepath, target_width, target_height=None):
    """Process logo: crop watermark, resize, 16-color. Transparent → colkey."""
    img = Image.open(filepath).convert("RGBA")
    w, h = img.size
    img = img.crop((0, 0, w - WATERMARK_CROP, h - WATERMARK_CROP))
    if target_height is None:
        ratio = target_width / img.width
        target_height = int(img.height * ratio)
    img = img.resize((target_width, target_height), Image.LANCZOS)
    result = Image.new("RGB", (target_width, target_height))
    src = img.load()
    dst = result.load()
    for y in range(target_height):
        for x in range(target_width):
            r, g, b, a = src[x, y]
            if a < 80:
                dst[x, y] = PYXEL_PALETTE[COLKEY]
            else:
                idx = nearest_palette_color(r, g, b)
                dst[x, y] = PYXEL_PALETTE[idx]
    return result, (target_width, target_height)


def build_backgrounds():
    """Build background + logo sprite sheet for Pyxel image bank 1."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    orig_dir = os.path.join(base_dir, "assets", "originals")
    out_path = os.path.join(base_dir, "assets", "bg_sprites.png")

    sheet = Image.new("RGB", (256, 256), PYXEL_PALETTE[COLKEY])

    for filename, pos in zip(BG_FILENAMES, BG_POSITIONS):
        filepath = os.path.join(orig_dir, filename)
        if not os.path.exists(filepath):
            print(f"WARNING: {filepath} not found, skipping")
            continue
        print(f"Processing {filename} → {BG_SIZE}...")
        bg = process_background(filepath, BG_SIZE)
        sheet.paste(bg, pos)
        print(f"  → at {pos}")

    logo_path = os.path.join(orig_dir, LOGO_FILENAME)
    if os.path.exists(logo_path):
        print(f"Processing {LOGO_FILENAME} → {LOGO_WIDTH}x{LOGO_HEIGHT}...")
        logo, logo_size = process_logo(logo_path, LOGO_WIDTH, LOGO_HEIGHT)
        sheet.paste(logo, LOGO_POS)
        print(f"  → at {LOGO_POS}, size={logo_size}")

    sheet.save(out_path)
    print(f"\nBG sprite sheet saved: {out_path}")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    orig_dir = os.path.join(base_dir, "assets", "originals")
    out_path = os.path.join(base_dir, "assets", "sprites.png")

    # Create sprite sheet (256x96: row 0 = 4x64x64, row 1 = small icons)
    sheet = Image.new("RGB", (256, SPRITE_SIZE + 32),
                      PYXEL_PALETTE[COLKEY])  # fill with colkey

    for i, filename in enumerate(CHARACTERS):
        filepath = os.path.join(orig_dir, filename)
        if not os.path.exists(filepath):
            print(f"WARNING: {filepath} not found, skipping")
            continue

        print(f"Processing {filename}...")
        sprite = process_character(filepath)
        sheet.paste(sprite, (i * SPRITE_SIZE, 0))
        print(f"  → slot {i} ({i * SPRITE_SIZE},0)")

    # Generate nabiko 32x32 icon at (0, 64)
    nabiko_path = os.path.join(orig_dir, "nabiko.png")
    if os.path.exists(nabiko_path):
        print("Processing nabiko 32x32 icon...")
        icon = process_character_small(nabiko_path, 32)
        sheet.paste(icon, (0, SPRITE_SIZE))
        print(f"  → icon at (0,{SPRITE_SIZE})")

    sheet.save(out_path)
    print(f"\nSprite sheet saved: {out_path}")
    print(f"Size: {sheet.size}")

    # Build background / logo sheet
    build_backgrounds()


if __name__ == "__main__":
    main()
