"""UI components for touch-based interaction."""

import pyxel


class Button:
    """Tappable button with label text."""

    def __init__(self, x, y, w, h, label):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = label

    def clicked(self):
        """Return True if button was tapped this frame."""
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            return self.x <= mx < self.x + self.w and self.y <= my < self.y + self.h
        return False

    def draw(self, font, col_bg=5, col_fg=7, col_border=6):
        """Draw the button with centered label."""
        pyxel.rect(self.x, self.y, self.w, self.h, col_bg)
        pyxel.rectb(self.x, self.y, self.w, self.h, col_border)
        if self.label:
            tw = font.text_width(self.label)
            tx = self.x + (self.w - tw) // 2
            ty = self.y + (self.h - 12) // 2
            pyxel.text(tx, ty, self.label, col_fg, font)


def text_centered(y, text, col, font):
    """Draw text horizontally centered on screen (240px wide)."""
    tw = font.text_width(text)
    pyxel.text(120 - tw // 2, y, text, col, font)


def draw_panel(x, y, w, h, col_bg=1, col_border=5):
    """Draw a rectangular panel."""
    pyxel.rect(x, y, w, h, col_bg)
    pyxel.rectb(x, y, w, h, col_border)
