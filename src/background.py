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
        """Home corner - dark cyber space with hologram panels and perspective grid."""
        # Full black background
        pyxel.rect(0, BG_TOP, WIDTH, BG_HEIGHT, C_BLACK)

        # ── Perspective grid floor (lower half) ──
        horizon_y = BG_TOP + 120  # horizon line
        floor_bottom = BG_BOTTOM

        # Horizontal grid lines (closer together near horizon, wider at bottom)
        num_hlines = 10
        for i in range(num_hlines):
            # Exponential spacing for perspective
            t = i / num_hlines
            y = int(horizon_y + (floor_bottom - horizon_y) * (t * t))
            pyxel.line(0, y, WIDTH - 1, y, C_DGRAY)

        # Vertical grid lines with perspective (converge toward center at horizon)
        cx = WIDTH // 2  # vanishing point x
        num_vlines = 12
        for i in range(num_vlines + 1):
            # Bottom x position (evenly spaced)
            bx = int(i * WIDTH / num_vlines)
            # At horizon, lines converge toward center
            tx = int(cx + (bx - cx) * 0.15)
            pyxel.line(tx, horizon_y, bx, floor_bottom, C_DGRAY)

        # ── Circuit pattern traces on floor (teal accents) ──
        rng = random.Random(42)  # deterministic
        for i in range(8):
            # Random horizontal circuit segments
            cy = int(horizon_y + 20 + i * 12)
            if cy >= floor_bottom:
                break
            sx = rng.randint(10, WIDTH - 80)
            length = rng.randint(20, 60)
            # Animate: some segments glow
            glow = math.sin(frame * 0.02 + i * 1.2) > 0.3
            col = C_SKYBLUE if glow else C_NAVY
            pyxel.line(sx, cy, sx + length, cy, col)
            # Small vertical branch
            if rng.random() > 0.4:
                branch_len = rng.randint(4, 12)
                bx = sx + rng.randint(5, length - 2) if length > 7 else sx + 3
                pyxel.line(bx, cy, bx, cy + branch_len, col)
            # Dot nodes at ends
            if glow:
                pyxel.pset(sx, cy, C_SKYBLUE)
                pyxel.pset(sx + length, cy, C_SKYBLUE)

        # ── Floating text fragments on floor (data residue) ──
        rng2 = random.Random(99)
        for i in range(4):
            ty = int(horizon_y + 30 + i * 22)
            if ty >= floor_bottom - 5:
                break
            tx = rng2.randint(5, WIDTH - 90)
            vis = math.sin(frame * 0.015 + i * 2.0) > 0.2
            if vis:
                # Tiny data lines (just short horizontal marks)
                for j in range(rng2.randint(2, 4)):
                    lw = rng2.randint(8, 25)
                    pyxel.line(tx + j * 4, ty + j * 4, tx + j * 4 + lw, ty + j * 4, C_NAVY)

        # ── Hologram panels (floating in upper dark space) ──

        # Panel 1: Large - dashboard with graph (center-right)
        self._draw_holo_panel_large(120, BG_TOP + 36, 100, 60, frame)

        # Panel 2: Small - data readout (left)
        self._draw_holo_panel_small(28, BG_TOP + 68, 50, 30, frame, phase=0.0)

        # Panel 3: Small - mini chart (right-lower)
        self._draw_holo_panel_small(175, BG_TOP + 80, 40, 24, frame, phase=2.0)

    def _draw_holo_panel_large(self, x, y, w, h, frame):
        """Draw a large holographic panel with graph and text lines."""
        # Semi-transparent fill (dark navy)
        pyxel.rect(x + 1, y + 1, w - 2, h - 2, C_NAVY)
        # Teal border
        pyxel.rectb(x, y, w, h, C_SKYBLUE)

        # Title bar line
        pyxel.line(x + 4, y + 4, x + w // 2 + 10, y + 4, C_SKYBLUE)

        # Text lines (left side)
        rng = random.Random(77)
        for i in range(5):
            ly = y + 10 + i * 7
            lw = rng.randint(15, 40)
            col = C_SKYBLUE if (frame // 40 + i) % 3 != 0 else C_NAVY
            pyxel.line(x + 6, ly, x + 6 + lw, ly, col)

        # Bar chart (right side)
        chart_x = x + w // 2 + 8
        chart_bottom = y + h - 6
        for i in range(5):
            bh = rng.randint(6, 28)
            # Animate bars slightly
            anim = math.sin(frame * 0.03 + i * 0.8) * 3
            bh = max(4, int(bh + anim))
            bx = chart_x + i * 8
            pyxel.rect(bx, chart_bottom - bh, 5, bh, C_SKYBLUE)
        # Chart baseline
        pyxel.line(chart_x - 2, chart_bottom, chart_x + 42, chart_bottom, C_DGRAY)

    def _draw_holo_panel_small(self, x, y, w, h, frame, phase=0.0):
        """Draw a small holographic panel with data lines."""
        pyxel.rect(x + 1, y + 1, w - 2, h - 2, C_NAVY)
        pyxel.rectb(x, y, w, h, C_SKYBLUE)

        # Data lines
        rng = random.Random(int(phase * 100 + 33))
        for i in range(3):
            ly = y + 5 + i * 7
            if ly >= y + h - 4:
                break
            lw = rng.randint(10, w - 12)
            col = C_SKYBLUE if math.sin(frame * 0.025 + phase + i) > 0.0 else C_NAVY
            pyxel.line(x + 4, ly, x + 4 + lw, ly, col)

        # Tiny bar or dot accent
        if h > 20:
            for i in range(3):
                bh = rng.randint(3, 10)
                bx = x + w - 16 + i * 5
                by = y + h - 4 - bh
                if bx < x + w - 3:
                    pyxel.rect(bx, by, 3, bh, C_SKYBLUE)

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
            (C_SKYBLUE, C_DGRAY, C_NAVY),                # 0: teal data motes
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
