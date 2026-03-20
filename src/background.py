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
    __slots__ = ('x', 'y', 'vy_base', 'phase', 'size')

    def __init__(self, x, y, vy_base, phase, size):
        self.x = x
        self.y = y
        self.vy_base = vy_base
        self.phase = phase
        self.size = size


class BackgroundRenderer:
    """Draws procedural backgrounds with particles for each office level."""

    def __init__(self):
        self.particles = self._create_particles(24)
        # Level-0 specific: 5 gentle floating particles in upper space
        self._lv0_particles = self._create_lv0_particles()

    def _create_particles(self, count):
        """Create a pool of particles with random positions (general use)."""
        pts = []
        for _ in range(count):
            pts.append(Particle(
                x=random.random() * WIDTH,
                y=random.random() * BG_HEIGHT + BG_TOP,
                vy_base=(random.random() - 0.5) * 0.15,
                phase=random.random() * 6.283,
                size=random.choice([0, 0, 0, 1]),
            ))
        return pts

    def _create_lv0_particles(self):
        """Create 5 gentle floating particles for level 0 upper space."""
        rng = random.Random(55)
        pts = []
        for _ in range(5):
            pts.append(Particle(
                x=rng.randint(15, WIDTH - 15),
                y=rng.randint(BG_TOP + 10, BG_TOP + 100),
                vy_base=rng.choice([-0.04, -0.03, 0.03, 0.04]),
                phase=rng.random() * 6.283,
                size=0,
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
        # Level 0 handles its own particles; others use general particles
        if idx > 0:
            self._draw_particles(frame, idx)

    # ── Helpers ──

    @staticmethod
    def _draw_dashed_line(x0, y0, x1, y1, col, dash=1, gap=1):
        """Draw a dashed line (1px on, 1px off) using pset."""
        dx = x1 - x0
        dy = y1 - y0
        length = max(abs(dx), abs(dy), 1)
        on = True
        count = 0
        for i in range(length + 1):
            t = i / length if length > 0 else 0
            px = int(x0 + dx * t)
            py = int(y0 + dy * t)
            if on:
                pyxel.pset(px, py, col)
            count += 1
            if on and count >= dash:
                on = False
                count = 0
            elif not on and count >= gap:
                on = True
                count = 0

    # ── Level 0: サイバー空間 ──

    def _draw_level0(self, frame):
        """Cyber space with perspective grid floor, window panels, circuit traces."""
        # Full black background
        pyxel.rect(0, BG_TOP, WIDTH, BG_HEIGHT, C_BLACK)

        # ── Perspective grid floor ──
        horizon_y = BG_TOP + 110
        floor_bottom = BG_BOTTOM
        floor_span = floor_bottom - horizon_y  # 130px
        cx = WIDTH // 2  # vanishing point x (center)
        # Vanishing point placed ABOVE the horizon so lines at the horizon
        # are already spread out, giving a gentler perspective
        vp_y = horizon_y - 10

        # Horizontal grid lines (wider spacing, exponential)
        # All solid lines — depth expressed by color only (dark→bright)
        num_hlines = 8
        for i in range(num_hlines):
            t = (i + 1) / (num_hlines + 1)
            y = int(horizon_y + floor_span * (t * t))
            col = C_NAVY if i < 5 else C_DGRAY
            pyxel.line(0, y, WIDTH - 1, y, col)

        # Vertical grid lines: fan out from vanishing point (above horizon)
        # Lines are clipped to start at horizon_y
        num_vlines = 30
        overshoot = 400
        total_span = floor_bottom - vp_y  # distance from VP to bottom

        # Color split at 40% down from horizon
        split_y = horizon_y + floor_span * 2 // 5
        split_t = (split_y - vp_y) / total_span
        # Clip top to horizon
        top_t = (horizon_y - vp_y) / total_span

        for i in range(num_vlines + 1):
            bx = int(-overshoot + i * (WIDTH + overshoot * 2) / num_vlines)

            # x at horizon (top of visible floor)
            top_x = int(cx + (bx - cx) * top_t)
            # x at color split point
            split_x = int(cx + (bx - cx) * split_t)

            # Far segment (horizon to split): dark
            pyxel.line(top_x, horizon_y, split_x, split_y, C_NAVY)
            # Near segment (split to bottom): brighter
            pyxel.line(split_x, split_y, bx, floor_bottom, C_DGRAY)

        # ── Hologram panels (window-style) ──
        self._draw_window_panel_large(115, BG_TOP + 30, 105, 65, frame)
        self._draw_window_panel_small(25, BG_TOP + 62, 55, 34, frame, phase=0.0)
        self._draw_window_panel_small(180, BG_TOP + 75, 48, 28, frame, phase=2.0)

        # ── Floating particles (upper space only) ──
        self._draw_lv0_particles(frame)

    def _draw_window_panel_large(self, x, y, w, h, frame):
        """Draw a large window-style panel with title bar, close button, data."""
        # Background fill (very dark)
        pyxel.rect(x + 1, y + 1, w - 2, h - 2, C_NAVY)
        # Border
        pyxel.rectb(x, y, w, h, C_SKYBLUE)

        # Title bar (top 5px strip)
        tb_h = 5
        pyxel.rect(x + 1, y + 1, w - 2, tb_h, C_DGRAY)
        # Title bar accent line
        pyxel.line(x + 3, y + 2, x + 25, y + 2, C_SKYBLUE)
        # Close button (3x3 square at right end of title bar)
        cb_x = x + w - 6
        cb_y = y + 1
        pyxel.rectb(cb_x, cb_y, 4, 4, C_SKYBLUE)

        # Content area starts below title bar
        content_y = y + tb_h + 2

        # Left side: text data lines (8 lines)
        rng = random.Random(77)
        for i in range(8):
            ly = content_y + i * 6
            if ly >= y + h - 4:
                break
            lw = rng.randint(10, 38)
            # Animate: some lines blink slowly
            vis = math.sin(frame * 0.018 + i * 0.9) > -0.3
            col = C_SKYBLUE if vis else C_NAVY
            pyxel.line(x + 4, ly, x + 4 + lw, ly, col)

        # Right side: bar chart (8 bars)
        chart_x = x + w // 2 + 6
        chart_bottom = y + h - 5
        num_bars = 8
        for i in range(num_bars):
            bh = rng.randint(5, 30)
            anim = math.sin(frame * 0.025 + i * 0.7) * 2
            bh = max(3, int(bh + anim))
            bx = chart_x + i * 6
            if bx + 4 > x + w - 3:
                break
            pyxel.rect(bx, chart_bottom - bh, 4, bh, C_SKYBLUE)
        # Chart baseline
        pyxel.line(chart_x - 1, chart_bottom, min(chart_x + num_bars * 6, x + w - 3), chart_bottom, C_DGRAY)

    def _draw_window_panel_small(self, x, y, w, h, frame, phase=0.0):
        """Draw a small window-style panel with title bar and data."""
        # Background
        pyxel.rect(x + 1, y + 1, w - 2, h - 2, C_NAVY)
        # Border
        pyxel.rectb(x, y, w, h, C_SKYBLUE)

        # Title bar
        tb_h = 4
        pyxel.rect(x + 1, y + 1, w - 2, tb_h, C_DGRAY)
        pyxel.line(x + 3, y + 2, x + 15, y + 2, C_SKYBLUE)
        # Close button
        cb_x = x + w - 5
        pyxel.rectb(cb_x, y + 1, 3, 3, C_SKYBLUE)

        # Content: data lines
        content_y = y + tb_h + 2
        rng = random.Random(int(phase * 100 + 33))
        for i in range(5):
            ly = content_y + i * 5
            if ly >= y + h - 4:
                break
            lw = rng.randint(8, w - 14)
            vis = math.sin(frame * 0.02 + phase + i * 0.8) > -0.2
            col = C_SKYBLUE if vis else C_NAVY
            pyxel.line(x + 3, ly, x + 3 + lw, ly, col)

        # Mini bar chart at bottom
        if h > 22:
            chart_bottom = y + h - 3
            for i in range(4):
                bh = rng.randint(2, 8)
                bx = x + w - 20 + i * 5
                if bx + 3 > x + w - 2:
                    break
                pyxel.rect(bx, chart_bottom - bh, 3, bh, C_SKYBLUE)

    def _draw_lv0_particles(self, frame):
        """Draw gentle floating particles in the upper dark space for level 0."""
        upper_top = BG_TOP + 5
        upper_bottom = BG_TOP + 105  # above horizon

        for i, p in enumerate(self._lv0_particles):
            # Slow vertical drift (sine-based oscillation)
            p.y += math.sin(frame * 0.015 + p.phase) * 0.08

            # Wrap within upper space
            if p.y < upper_top:
                p.y = upper_bottom - 1
            elif p.y >= upper_bottom:
                p.y = upper_top + 1

            # Soft blink (mostly visible, gentle fade)
            alpha = math.sin(frame * 0.02 + p.phase)
            if alpha > -0.5:
                col = C_SKYBLUE if i % 2 == 0 else C_DGRAY
                ix, iy = int(p.x), int(p.y)
                pyxel.pset(ix, iy, col)

    # ── Level 1-4: Placeholder (to be implemented) ──

    def _draw_level1(self, frame):
        """Placeholder: ワンルーム."""
        pyxel.rect(0, BG_TOP, WIDTH, BG_HEIGHT, C_BLACK)
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

    # ── Particles (for levels 1-4) ──

    def _draw_particles(self, frame, level):
        """Animate and draw floating light particles (levels 1-4)."""
        counts = (0, 8, 12, 16, 20)  # level 0 uses its own particles
        palettes = (
            (C_SKYBLUE,),                              # 0: unused
            (C_GRAY, C_SKYBLUE),                       # 1: cool
            (C_SKYBLUE, C_GREEN),                      # 2: digital
            (C_SKYBLUE, C_YELLOW, C_GREEN),            # 3: vibrant
            (C_YELLOW, C_WHITE, C_SKYBLUE, C_LAVENDER),  # 4: radiant
        )

        lvl = min(level, 4)
        count = counts[lvl]
        if count == 0:
            return
        colors = palettes[lvl]

        for i in range(min(count, len(self.particles))):
            p = self.particles[i]
            p.y += p.vy_base
            if p.y < BG_TOP:
                p.y = BG_BOTTOM - 1
            elif p.y >= BG_BOTTOM:
                p.y = BG_TOP

            alpha = math.sin(frame * 0.03 + p.phase)
            if alpha > -0.2:
                col = colors[i % len(colors)]
                ix, iy = int(p.x), int(p.y)
                pyxel.pset(ix, iy, col)
                if p.size > 0 and alpha > 0.5:
                    pyxel.pset(ix + 1, iy, col)
                    pyxel.pset(ix, iy + 1, col)
