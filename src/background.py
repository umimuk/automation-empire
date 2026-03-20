"""Procedural background drawing for each office level.

Replaces bg_sprites.png with code-drawn backgrounds using
pyxel.rect(), line(), pset() for grid lines, floating panels,
and animated particles.
"""

import pyxel
import math
import random

from src.constants import (
    WIDTH,
    C_BLACK, C_NAVY, C_PURPLE, C_DGREEN, C_BROWN, C_DGRAY, C_GRAY, C_WHITE,
    C_RED, C_ORANGE, C_YELLOW, C_GREEN, C_SKYBLUE, C_LAVENDER, C_PINK, C_PEACH,
)

# Background drawing area (below status bar, above text)
BG_TOP = 24
BG_HEIGHT = 240
BG_BOTTOM = BG_TOP + BG_HEIGHT


class Particle:
    """A single floating light particle."""
    __slots__ = ('x', 'y', 'vx', 'vy', 'phase', 'size')

    def __init__(self, x, y, vx, vy, phase, size):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.phase = phase
        self.size = size


class BackgroundRenderer:
    """Draws procedural backgrounds with particles for each office level."""

    def __init__(self):
        self.particles = self._create_particles(24)

    def _create_particles(self, count):
        """Create a pool of particles with random positions."""
        pts = []
        for _ in range(count):
            pts.append(Particle(
                x=random.random() * WIDTH,
                y=random.random() * BG_HEIGHT + BG_TOP,
                vx=(random.random() - 0.5) * 0.3,
                vy=-random.random() * 0.2 - 0.05,
                phase=random.random() * 6.283,
                size=random.choice([0, 0, 0, 1]),
            ))
        return pts

    # ── Public API ──

    def draw(self, office_level, frame):
        """Draw the background for the given office level."""
        draw_fn = (
            self._draw_level0,
            self._draw_level1,
            self._draw_level2,
            self._draw_level3,
            self._draw_level4,
        )
        idx = min(office_level, len(draw_fn) - 1)
        draw_fn[idx](frame)
        self._draw_particles(frame, office_level)

    # ── Level 0: 自宅の一角 ──

    def _draw_level0(self, frame):
        """Home corner - dark cozy room with desk and monitor."""
        # Dark room base
        pyxel.rect(0, BG_TOP, WIDTH, BG_HEIGHT, C_BLACK)

        # Faint grid on wall (cyberpunk hint)
        for x in range(0, WIDTH, 27):
            pyxel.line(x, BG_TOP, x, BG_TOP + 155, C_NAVY)
        for y in range(BG_TOP, BG_TOP + 156, 27):
            pyxel.line(0, y, WIDTH, y, C_NAVY)

        # Floor
        floor_y = BG_TOP + 156
        pyxel.rect(0, floor_y, WIDTH, BG_BOTTOM - floor_y, C_BROWN)
        # Floor highlight line
        pyxel.line(0, floor_y, WIDTH, floor_y, C_DGRAY)
        # Floor texture - subtle horizontal lines
        for fy in range(floor_y + 12, BG_BOTTOM, 12):
            pyxel.line(0, fy, WIDTH, fy, C_DGRAY)

        # ── Desk ──
        desk_x, desk_w = 55, 160
        desk_top = BG_TOP + 130
        desk_h = 26
        # Desk surface
        pyxel.rect(desk_x, desk_top, desk_w, desk_h, C_DGRAY)
        pyxel.rectb(desk_x, desk_top, desk_w, desk_h, C_GRAY)
        # Desk legs
        pyxel.rect(desk_x + 6, desk_top + desk_h, 6, 20, C_DGRAY)
        pyxel.rect(desk_x + desk_w - 12, desk_top + desk_h, 6, 20, C_DGRAY)

        # ── Monitor ──
        mon_x = desk_x + 55
        mon_w, mon_h = 50, 36
        mon_y = desk_top - mon_h - 6
        # Monitor body
        pyxel.rect(mon_x, mon_y, mon_w, mon_h, C_DGRAY)
        pyxel.rectb(mon_x, mon_y, mon_w, mon_h, C_GRAY)
        # Screen with glow animation
        glow = math.sin(frame * 0.04) * 0.5 + 0.5
        screen_col = C_SKYBLUE if glow > 0.5 else C_NAVY
        pyxel.rect(mon_x + 3, mon_y + 3, mon_w - 6, mon_h - 8, screen_col)
        # Code lines on screen
        if glow > 0.3:
            for i in range(3):
                lw = 10 + (i * 7 + frame // 30) % 20
                ly = mon_y + 6 + i * 7
                pyxel.line(mon_x + 6, ly, mon_x + 6 + lw, ly, C_GREEN)
        # Monitor stand
        stand_x = mon_x + mon_w // 2 - 4
        pyxel.rect(stand_x, mon_y + mon_h, 8, 6, C_DGRAY)

        # ── Keyboard on desk ──
        kb_x = mon_x - 5
        kb_y = desk_top + 4
        pyxel.rect(kb_x, kb_y, 30, 8, C_DGRAY)
        pyxel.rectb(kb_x, kb_y, 30, 8, C_GRAY)

        # ── Coffee mug ──
        mug_x = desk_x + 12
        mug_y = desk_top + 3
        pyxel.rect(mug_x, mug_y, 10, 12, C_BROWN)
        pyxel.rectb(mug_x, mug_y, 10, 12, C_DGRAY)
        # Steam animation
        steam_offset = (frame // 8) % 3
        pyxel.pset(mug_x + 3, mug_y - 2 - steam_offset, C_GRAY)
        pyxel.pset(mug_x + 7, mug_y - 3 - steam_offset, C_GRAY)

        # ── Small window (upper right) ──
        win_x, win_y = 205, BG_TOP + 16
        win_w, win_h = 44, 50
        pyxel.rect(win_x, win_y, win_w, win_h, C_DGRAY)
        pyxel.rectb(win_x, win_y, win_w, win_h, C_GRAY)
        # Window cross
        pyxel.line(win_x + win_w // 2, win_y, win_x + win_w // 2, win_y + win_h, C_GRAY)
        pyxel.line(win_x, win_y + win_h // 2, win_x + win_w, win_y + win_h // 2, C_GRAY)
        # Night sky
        pyxel.rect(win_x + 2, win_y + 2, win_w // 2 - 3, win_h // 2 - 3, C_BLACK)
        pyxel.rect(win_x + win_w // 2 + 1, win_y + 2, win_w // 2 - 3, win_h // 2 - 3, C_BLACK)
        pyxel.rect(win_x + 2, win_y + win_h // 2 + 1, win_w // 2 - 3, win_h // 2 - 3, C_BLACK)
        pyxel.rect(win_x + win_w // 2 + 1, win_y + win_h // 2 + 1, win_w // 2 - 3, win_h // 2 - 3, C_BLACK)
        # Stars blinking
        if frame % 80 < 55:
            pyxel.pset(win_x + 8, win_y + 10, C_WHITE)
            pyxel.pset(win_x + 32, win_y + 8, C_WHITE)
        if frame % 90 < 40:
            pyxel.pset(win_x + 18, win_y + 36, C_GRAY)

        # ── Bookshelf (left wall) ──
        shelf_x = 10
        shelf_y = BG_TOP + 30
        shelf_w, shelf_h = 35, 90
        pyxel.rect(shelf_x, shelf_y, shelf_w, shelf_h, C_DGRAY)
        pyxel.rectb(shelf_x, shelf_y, shelf_w, shelf_h, C_GRAY)
        # Shelf dividers
        for sy in range(shelf_y + 22, shelf_y + shelf_h, 22):
            pyxel.line(shelf_x + 1, sy, shelf_x + shelf_w - 1, sy, C_GRAY)
        # Books (colored rectangles)
        book_colors = [C_RED, C_SKYBLUE, C_GREEN, C_PURPLE, C_ORANGE,
                       C_YELLOW, C_PINK, C_NAVY, C_DGREEN]
        bi = 0
        for row in range(3):
            by = shelf_y + 3 + row * 22
            bx = shelf_x + 3
            for _ in range(4):
                bw = random.Random(bi + 42).randint(4, 7)
                pyxel.rect(bx, by, bw, 18, book_colors[bi % len(book_colors)])
                bx += bw + 1
                bi += 1

        # ── Ambient glow from monitor ──
        # Soft glow on desk area
        if glow > 0.4:
            for dx in range(-8, 9, 4):
                gx = mon_x + mon_w // 2 + dx
                pyxel.pset(gx, desk_top - 2, C_NAVY)

    # ── Level 1-4: Placeholder (to be implemented) ──

    def _draw_level1(self, frame):
        """Placeholder: ワンルーム."""
        pyxel.rect(0, BG_TOP, WIDTH, BG_HEIGHT, C_BLACK)
        # Simple grid
        for x in range(0, WIDTH, 20):
            pyxel.line(x, BG_TOP, x, BG_BOTTOM, C_NAVY)
        for y in range(BG_TOP, BG_BOTTOM, 20):
            pyxel.line(0, y, WIDTH, y, C_NAVY)

    def _draw_level2(self, frame):
        """Placeholder: フロアオフィス."""
        pyxel.rect(0, BG_TOP, WIDTH, BG_HEIGHT, C_NAVY)
        for x in range(0, WIDTH, 18):
            pyxel.line(x, BG_TOP, x, BG_BOTTOM, C_DGRAY)
        for y in range(BG_TOP, BG_BOTTOM, 18):
            pyxel.line(0, y, WIDTH, y, C_DGRAY)

    def _draw_level3(self, frame):
        """Placeholder: ビル1棟."""
        pyxel.rect(0, BG_TOP, WIDTH, BG_HEIGHT, C_NAVY)
        for x in range(0, WIDTH, 15):
            pyxel.line(x, BG_TOP, x, BG_BOTTOM, C_PURPLE)
        for y in range(BG_TOP, BG_BOTTOM, 15):
            pyxel.line(0, y, WIDTH, y, C_PURPLE)

    def _draw_level4(self, frame):
        """Placeholder: AI帝国タワー."""
        pyxel.rect(0, BG_TOP, WIDTH, BG_HEIGHT, C_BLACK)
        for x in range(0, WIDTH, 12):
            pyxel.line(x, BG_TOP, x, BG_BOTTOM, C_PURPLE)
        for y in range(BG_TOP, BG_BOTTOM, 12):
            pyxel.line(0, y, WIDTH, y, C_PURPLE)

    # ── Particles ──

    def _draw_particles(self, frame, level):
        """Animate and draw floating light particles."""
        # Particle count and colors per level
        counts = (5, 8, 12, 16, 20)
        palettes = (
            (C_DGRAY, C_GRAY),                       # 0: dim dust
            (C_GRAY, C_SKYBLUE),                      # 1: cool
            (C_SKYBLUE, C_GREEN),                     # 2: digital
            (C_SKYBLUE, C_YELLOW, C_GREEN),           # 3: vibrant
            (C_YELLOW, C_WHITE, C_SKYBLUE, C_LAVENDER),  # 4: radiant
        )

        lvl = min(level, 4)
        count = counts[lvl]
        colors = palettes[lvl]

        for i in range(min(count, len(self.particles))):
            p = self.particles[i]

            # Move
            p.x += p.vx
            p.y += p.vy

            # Wrap
            if p.x < 0:
                p.x = WIDTH - 1
            elif p.x >= WIDTH:
                p.x = 0
            if p.y < BG_TOP:
                p.y = BG_BOTTOM - 1
            elif p.y >= BG_BOTTOM:
                p.y = BG_TOP

            # Blink
            alpha = math.sin(frame * 0.03 + p.phase)
            if alpha > -0.2:
                col = colors[i % len(colors)]
                ix, iy = int(p.x), int(p.y)
                pyxel.pset(ix, iy, col)
                if p.size > 0 and alpha > 0.5:
                    pyxel.pset(ix + 1, iy, col)
                    pyxel.pset(ix, iy + 1, col)
