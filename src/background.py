"""Procedural background drawing for each office level.

Draws grid floors, hologram panels, city silhouettes, data streams,
circuit traces, and particles — all via pyxel draw primitives.
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

# Shared grid constants
_HORIZON_Y = BG_TOP + 110
_VP_OFFSET = 10  # vanishing point pixels above horizon


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
        self._lv0_particles = self._create_lv0_particles(5)
        self._title_particles = self._create_title_particles()

    @staticmethod
    def _create_particles(count):
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

    @staticmethod
    def _create_lv0_particles(count):
        rng = random.Random(55)
        pts = []
        for _ in range(count):
            pts.append(Particle(
                x=rng.randint(15, WIDTH - 15),
                y=rng.randint(BG_TOP + 10, BG_TOP + 100),
                vy_base=rng.choice([-0.04, -0.03, 0.03, 0.04]),
                phase=rng.random() * 6.283,
                size=0,
            ))
        return pts

    @staticmethod
    def _create_title_particles():
        rng = random.Random(777)
        pts = []
        for _ in range(12):
            pts.append(Particle(
                x=rng.randint(10, WIDTH - 10),
                y=rng.randint(30, 400),
                vy_base=rng.choice([-0.06, -0.04, -0.03, 0.03, 0.04, 0.06]),
                phase=rng.random() * 6.283,
                size=rng.choice([0, 0, 1]),
            ))
        return pts

    # ── Public API ──

    def draw(self, office_level, frame):
        draw_fn = (
            self._draw_level0, self._draw_level1, self._draw_level2,
            self._draw_level3, self._draw_level4,
        )
        idx = min(office_level, len(draw_fn) - 1)
        draw_fn[idx](frame)
        if idx > 0:
            self._draw_particles(frame, idx)

    def draw_title_bg(self, frame):
        """Draw title screen background with particles."""
        pyxel.cls(C_BLACK)
        # Subtle grid at the bottom (mini version of floor)
        for y in range(350, 480, 18):
            a = (y - 350) / 130.0
            col = C_NAVY if a < 0.5 else C_DGRAY
            pyxel.line(0, y, WIDTH - 1, y, col)
        cx = WIDTH // 2
        for i in range(12):
            bx = int(-60 + i * (WIDTH + 120) / 11)
            pyxel.line(cx, 340, bx, 480, C_NAVY)
        # Title particles
        for i, p in enumerate(self._title_particles):
            p.y += math.sin(frame * 0.012 + p.phase) * 0.12
            if p.y < 20:
                p.y = 420
            elif p.y > 430:
                p.y = 30
            alpha = math.sin(frame * 0.025 + p.phase)
            if alpha > -0.3:
                col = [C_SKYBLUE, C_DGRAY, C_LAVENDER][i % 3]
                ix, iy = int(p.x), int(p.y)
                pyxel.pset(ix, iy, col)
                if p.size > 0 and alpha > 0.5:
                    pyxel.pset(ix + 1, iy, col)

    # ══════════════════════════════════════════
    # Shared drawing helpers
    # ══════════════════════════════════════════

    def _draw_grid_floor(self, col_far, col_near,
                         accent_col=None, accent_h_indices=None):
        """Draw perspective grid floor. accent applies to specific h-lines."""
        horizon_y = _HORIZON_Y
        floor_bottom = BG_BOTTOM
        floor_span = floor_bottom - horizon_y
        cx = WIDTH // 2
        vp_y = horizon_y - _VP_OFFSET
        total_span = floor_bottom - vp_y

        # Horizontal lines
        for i in range(8):
            t = (i + 1) / 9
            y = int(horizon_y + floor_span * (t * t))
            if accent_col and accent_h_indices and i in accent_h_indices:
                col = accent_col
            elif i < 5:
                col = col_far
            else:
                col = col_near
            pyxel.line(0, y, WIDTH - 1, y, col)

        # Vertical lines
        overshoot = 400
        split_y = horizon_y + floor_span * 2 // 5
        split_t = (split_y - vp_y) / total_span
        top_t = (horizon_y - vp_y) / total_span

        for i in range(31):
            bx = int(-overshoot + i * (WIDTH + overshoot * 2) / 30)
            top_x = int(cx + (bx - cx) * top_t)
            split_x = int(cx + (bx - cx) * split_t)
            pyxel.line(top_x, horizon_y, split_x, split_y, col_far)
            pyxel.line(split_x, split_y, bx, floor_bottom, col_near)

    def _draw_window_panel(self, x, y, w, h, frame, phase=0.0,
                           col=C_SKYBLUE, large=False):
        """Draw a window-style hologram panel (unified method)."""
        # Background + border
        pyxel.rect(x + 1, y + 1, w - 2, h - 2, C_NAVY)
        pyxel.rectb(x, y, w, h, col)

        # Title bar
        tb_h = 5 if large else 4
        pyxel.rect(x + 1, y + 1, w - 2, tb_h, C_DGRAY)
        pyxel.line(x + 3, y + 2, x + min(25, w // 3), y + 2, col)
        # Close button
        cb_sz = 4 if large else 3
        pyxel.rectb(x + w - cb_sz - 2, y + 1, cb_sz, cb_sz, col)

        content_y = y + tb_h + 2
        rng = random.Random(int(phase * 100 + w * 7 + 33))

        if large:
            # Left: text lines
            for i in range(8):
                ly = content_y + i * 6
                if ly >= y + h - 4:
                    break
                lw = rng.randint(10, min(38, w // 2 - 8))
                vis = math.sin(frame * 0.018 + phase + i * 0.9) > -0.3
                pyxel.line(x + 4, ly, x + 4 + lw, ly, col if vis else C_NAVY)
            # Right: bar chart
            chart_x = x + w // 2 + 6
            chart_bottom = y + h - 5
            for i in range(8):
                bh = rng.randint(5, 30)
                anim = math.sin(frame * 0.025 + phase + i * 0.7) * 2
                bh = max(3, int(bh + anim))
                bx2 = chart_x + i * 6
                if bx2 + 4 > x + w - 3:
                    break
                pyxel.rect(bx2, chart_bottom - bh, 4, bh, col)
            pyxel.line(chart_x - 1, chart_bottom,
                       min(chart_x + 48, x + w - 3), chart_bottom, C_DGRAY)
        else:
            # Text lines
            for i in range(5):
                ly = content_y + i * 5
                if ly >= y + h - 4:
                    break
                lw = rng.randint(8, w - 14)
                vis = math.sin(frame * 0.02 + phase + i * 0.8) > -0.2
                pyxel.line(x + 3, ly, x + 3 + lw, ly, col if vis else C_NAVY)
            # Mini bars
            if h > 22:
                chart_bottom = y + h - 3
                for i in range(4):
                    bh = rng.randint(2, 8)
                    bx2 = x + w - 20 + i * 5
                    if bx2 + 3 > x + w - 2:
                        break
                    pyxel.rect(bx2, chart_bottom - bh, 3, bh, col)

    def _draw_data_streams(self, frame, streams):
        """Horizontal flowing data segments.
        streams: list of (y, speed, col, seed)
        """
        for sy, speed, col, seed in streams:
            rng = random.Random(seed)
            offset = int(frame * speed) % (WIDTH + 80)
            for _ in range(5):
                sx = (rng.randint(0, WIDTH) + offset) % (WIDTH + 80) - 40
                sw = rng.randint(12, 35)
                x0 = max(0, sx)
                x1 = min(WIDTH - 1, sx + sw)
                if x0 < x1:
                    pyxel.line(x0, sy, x1, sy, col)

    def _draw_city_silhouette(self, col, num_buildings, max_h=25,
                              lit_col=None):
        """Draw building outlines at the horizon."""
        horizon_y = _HORIZON_Y
        rng = random.Random(99)
        for _ in range(num_buildings):
            bx = rng.randint(0, WIDTH - 8)
            bw = rng.randint(5, 18)
            bh = rng.randint(6, max_h)
            by = horizon_y - bh
            pyxel.rectb(bx, by, bw, bh, col)
            # Antenna/spire on tall buildings
            if bh > 18:
                ax = bx + bw // 2
                pyxel.line(ax, by, ax, by - 3, col)
            # Windows (tiny dots)
            wc = lit_col or col
            if bh > 10 and bw > 8:
                for wy in range(by + 3, by + bh - 2, 4):
                    for wx in range(bx + 2, bx + bw - 2, 4):
                        pyxel.pset(wx, wy, wc)

    def _draw_floor_circuits(self, frame, col, count):
        """Glowing circuit segments on the floor."""
        rng = random.Random(42)
        for i in range(count):
            cy = rng.randint(_HORIZON_Y + 25, BG_BOTTOM - 10)
            sx = rng.randint(5, WIDTH - 50)
            seg_len = rng.randint(12, 40)
            glow = (math.sin(frame * 0.012 + i * 1.5) + 1.0) * 0.5
            if glow > 0.35:
                pyxel.line(sx, cy, sx + seg_len, cy, col)
                pyxel.pset(sx, cy, col)
                pyxel.pset(sx + seg_len, cy, col)
                # Perpendicular stub
                if rng.random() > 0.5:
                    stub = rng.randint(3, 8)
                    pyxel.line(sx + seg_len, cy,
                               sx + seg_len, cy - stub, col)

    def _draw_crown(self, cx, y, col):
        """Pixel art crown at top of screen."""
        # Base band
        pyxel.rect(cx - 10, y + 8, 21, 3, col)
        # Crown body
        pyxel.rect(cx - 8, y + 5, 17, 3, col)
        # 5 pointed peaks
        for i in range(5):
            px = cx - 8 + i * 4
            pyxel.rect(px, y + 1, 3, 4, col)
            pyxel.pset(px + 1, y, col)

    def _draw_horizon_glow(self, col):
        """Bright line at the horizon representing city light."""
        pyxel.line(0, _HORIZON_Y, WIDTH - 1, _HORIZON_Y, col)
        # Faint glow above
        pyxel.line(0, _HORIZON_Y - 1, WIDTH - 1, _HORIZON_Y - 1, C_NAVY)

    # ══════════════════════════════════════════
    # Level 0: 自宅の一角 — Minimal cyber space
    # ══════════════════════════════════════════

    def _draw_level0(self, frame):
        pyxel.rect(0, BG_TOP, WIDTH, BG_HEIGHT, C_BLACK)
        self._draw_grid_floor(C_NAVY, C_DGRAY)
        # 3 panels
        self._draw_window_panel(115, BG_TOP + 30, 105, 65, frame,
                                large=True)
        self._draw_window_panel(25, BG_TOP + 62, 55, 34, frame, phase=0.5)
        self._draw_window_panel(180, BG_TOP + 75, 48, 28, frame, phase=2.0)
        # 5 gentle floating particles
        self._draw_upper_particles(frame, self._lv0_particles)

    # ══════════════════════════════════════════
    # Level 1: ワンルーム — Growing operation
    # ══════════════════════════════════════════

    def _draw_level1(self, frame):
        pyxel.rect(0, BG_TOP, WIDTH, BG_HEIGHT, C_BLACK)
        # Data streams near horizon (before grid so grid draws over)
        self._draw_data_streams(frame, [
            (_HORIZON_Y - 3, 0.3, C_SKYBLUE, 10),
            (_HORIZON_Y + 3, 0.2, C_NAVY, 20),
        ])
        # Grid with accent on bottom 2 lines
        self._draw_grid_floor(C_NAVY, C_DGRAY, C_SKYBLUE, {6, 7})
        # 5 panels (2 large, 3 small)
        self._draw_window_panel(100, BG_TOP + 22, 108, 65, frame,
                                large=True)
        self._draw_window_panel(3, BG_TOP + 36, 88, 55, frame,
                                phase=1.0, large=True)
        self._draw_window_panel(30, BG_TOP + 6, 55, 28, frame, phase=0.5)
        self._draw_window_panel(195, BG_TOP + 52, 50, 28, frame, phase=1.5)
        self._draw_window_panel(170, BG_TOP + 86, 52, 26, frame, phase=3.0)

    # ══════════════════════════════════════════
    # Level 2: フロアオフィス — City emerging
    # ══════════════════════════════════════════

    def _draw_level2(self, frame):
        pyxel.rect(0, BG_TOP, WIDTH, BG_HEIGHT, C_BLACK)
        # Faint city
        self._draw_city_silhouette(C_NAVY, 8, max_h=20)
        # Data streams
        self._draw_data_streams(frame, [
            (_HORIZON_Y - 6, 0.4, C_SKYBLUE, 10),
            (_HORIZON_Y - 2, 0.3, C_PURPLE, 15),
            (_HORIZON_Y + 4, 0.2, C_SKYBLUE, 20),
        ])
        # Grid + purple accent
        self._draw_grid_floor(C_NAVY, C_DGRAY, C_PURPLE, {5, 6})
        # Sparse floor circuits
        self._draw_floor_circuits(frame, C_SKYBLUE, 4)
        # 7 panels (2 large, 5 small)  — some with purple borders
        self._draw_window_panel(90, BG_TOP + 15, 112, 65, frame,
                                large=True)
        self._draw_window_panel(0, BG_TOP + 28, 85, 55, frame,
                                phase=1.0, large=True)
        self._draw_window_panel(40, BG_TOP + 3, 52, 26, frame, phase=0.2)
        self._draw_window_panel(200, BG_TOP + 6, 48, 24, frame,
                                phase=0.5, col=C_PURPLE)
        self._draw_window_panel(185, BG_TOP + 46, 55, 30, frame, phase=1.5)
        self._draw_window_panel(10, BG_TOP + 88, 52, 26, frame,
                                phase=2.0, col=C_PURPLE)
        self._draw_window_panel(200, BG_TOP + 80, 50, 28, frame, phase=3.0)

    # ══════════════════════════════════════════
    # Level 3: ビル1棟 — Full operation
    # ══════════════════════════════════════════

    def _draw_level3(self, frame):
        pyxel.rect(0, BG_TOP, WIDTH, BG_HEIGHT, C_BLACK)
        # Clear city silhouette
        self._draw_city_silhouette(C_DGRAY, 15, max_h=40,
                                   lit_col=C_SKYBLUE)
        self._draw_horizon_glow(C_SKYBLUE)
        # Data streams (multiple)
        self._draw_data_streams(frame, [
            (_HORIZON_Y - 10, 0.5, C_SKYBLUE, 10),
            (_HORIZON_Y - 5, 0.4, C_PURPLE, 15),
            (_HORIZON_Y, 0.35, C_SKYBLUE, 20),
            (_HORIZON_Y + 5, 0.25, C_YELLOW, 25),
        ])
        # Grid with gold accent lines
        self._draw_grid_floor(C_DGRAY, C_GRAY, C_YELLOW, {5, 6, 7})
        # Complex circuits
        self._draw_floor_circuits(frame, C_YELLOW, 8)
        # 10 panels (3 large, 7 small) — mixed colors
        self._draw_window_panel(75, BG_TOP + 10, 118, 65, frame,
                                large=True)
        self._draw_window_panel(0, BG_TOP + 18, 72, 48, frame,
                                phase=0.8, large=True, col=C_SKYBLUE)
        self._draw_window_panel(178, BG_TOP + 30, 88, 52, frame,
                                phase=1.5, large=True)
        self._draw_window_panel(5, BG_TOP + 2, 55, 22, frame, phase=0.2)
        self._draw_window_panel(140, BG_TOP + 2, 48, 20, frame,
                                phase=0.5, col=C_YELLOW)
        self._draw_window_panel(215, BG_TOP + 2, 50, 22, frame, phase=1.0)
        self._draw_window_panel(15, BG_TOP + 72, 55, 28, frame,
                                phase=1.8, col=C_PURPLE)
        self._draw_window_panel(80, BG_TOP + 80, 50, 24, frame, phase=2.2)
        self._draw_window_panel(200, BG_TOP + 86, 58, 28, frame,
                                phase=2.8, col=C_YELLOW)
        self._draw_window_panel(145, BG_TOP + 80, 52, 22, frame, phase=3.2)

    # ══════════════════════════════════════════
    # Level 4: AI帝国タワー — The Empire
    # ══════════════════════════════════════════

    def _draw_level4(self, frame):
        pyxel.rect(0, BG_TOP, WIDTH, BG_HEIGHT, C_BLACK)
        # Crown at top
        self._draw_crown(WIDTH // 2, BG_TOP + 3, C_YELLOW)
        # Massive city (two layers for depth)
        self._draw_city_silhouette(C_NAVY, 12, max_h=55)
        self._draw_city_silhouette(C_DGRAY, 10, max_h=42,
                                   lit_col=C_SKYBLUE)
        self._draw_horizon_glow(C_SKYBLUE)
        # Data streams everywhere
        self._draw_data_streams(frame, [
            (_HORIZON_Y - 14, 0.6, C_SKYBLUE, 10),
            (_HORIZON_Y - 9, 0.5, C_PURPLE, 15),
            (_HORIZON_Y - 4, 0.45, C_SKYBLUE, 20),
            (_HORIZON_Y, 0.4, C_YELLOW, 25),
            (_HORIZON_Y + 6, 0.3, C_PURPLE, 30),
            (_HORIZON_Y + 12, 0.25, C_SKYBLUE, 35),
        ])
        # Grid with gold
        self._draw_grid_floor(C_DGRAY, C_GRAY, C_YELLOW, {4, 5, 6, 7})
        # Dense circuits
        self._draw_floor_circuits(frame, C_YELLOW, 12)
        # 12 panels — all over the place
        self._draw_window_panel(65, BG_TOP + 16, 125, 68, frame,
                                large=True)
        self._draw_window_panel(0, BG_TOP + 18, 62, 44, frame,
                                phase=0.8, large=True, col=C_SKYBLUE)
        self._draw_window_panel(195, BG_TOP + 14, 72, 50, frame,
                                phase=1.5, large=True, col=C_YELLOW)
        self._draw_window_panel(5, BG_TOP + 2, 52, 18, frame,
                                phase=0.1, col=C_PINK)
        self._draw_window_panel(62, BG_TOP + 2, 46, 16, frame, phase=0.4)
        self._draw_window_panel(205, BG_TOP + 2, 48, 18, frame,
                                phase=0.7, col=C_YELLOW)
        self._draw_window_panel(5, BG_TOP + 68, 58, 28, frame,
                                phase=1.2, col=C_PURPLE)
        self._draw_window_panel(68, BG_TOP + 78, 52, 24, frame, phase=1.8)
        self._draw_window_panel(140, BG_TOP + 74, 58, 28, frame,
                                phase=2.2, col=C_YELLOW)
        self._draw_window_panel(205, BG_TOP + 70, 55, 26, frame,
                                phase=2.6, col=C_PINK)
        self._draw_window_panel(28, BG_TOP + 96, 48, 20, frame,
                                phase=3.0)
        self._draw_window_panel(178, BG_TOP + 96, 52, 22, frame,
                                phase=3.5, col=C_PURPLE)

    # ══════════════════════════════════════════
    # Particle systems
    # ══════════════════════════════════════════

    def _draw_upper_particles(self, frame, particles):
        """Gentle floating particles in the upper dark space (level 0)."""
        upper_top = BG_TOP + 5
        upper_bottom = BG_TOP + 105

        for i, p in enumerate(particles):
            p.y += math.sin(frame * 0.015 + p.phase) * 0.08
            if p.y < upper_top:
                p.y = upper_bottom - 1
            elif p.y >= upper_bottom:
                p.y = upper_top + 1
            alpha = math.sin(frame * 0.02 + p.phase)
            if alpha > -0.5:
                col = C_SKYBLUE if i % 2 == 0 else C_DGRAY
                pyxel.pset(int(p.x), int(p.y), col)

    def _draw_particles(self, frame, level):
        """Animate and draw floating particles (levels 1-4)."""
        counts = (0, 8, 10, 15, 20)
        palettes = (
            (C_SKYBLUE,),
            (C_GRAY, C_SKYBLUE),
            (C_SKYBLUE, C_GREEN, C_PURPLE),
            (C_SKYBLUE, C_YELLOW, C_GREEN, C_PURPLE),
            (C_YELLOW, C_WHITE, C_SKYBLUE, C_LAVENDER, C_PINK),
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
