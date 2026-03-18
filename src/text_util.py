"""テキスト描画ユーティリティ（日本語対応）"""

import pyxel

# Pyxelのビルトインフォントは英数のみ。
# 日本語は pyxel.text() では表示できないため、
# 英語フォールバック + カタカナマッピングで対応する。
# 将来的にはカスタムフォントスプライトで完全日本語対応。

# 現時点では英語テキストで開発を進め、
# ドット絵フォント完成後に日本語化する。

# シンプルなテキスト描画ラッパー
def draw_text(x, y, text, col=7):
    """テキスト描画（改行対応）"""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        pyxel.text(x, y + i * 8, line, col)


def draw_text_center(y, text, col=7):
    """中央揃えテキスト描画"""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        w = len(line) * 4  # Pyxelフォントは1文字4px幅
        x = (256 - w) // 2
        pyxel.text(x, y + i * 8, line, col)


def draw_text_shadow(x, y, text, col=7, shadow_col=0):
    """影付きテキスト"""
    draw_text(x + 1, y + 1, text, shadow_col)
    draw_text(x, y, text, col)


def draw_text_center_shadow(y, text, col=7, shadow_col=0):
    """中央揃え影付きテキスト"""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        w = len(line) * 4
        x = (256 - w) // 2
        pyxel.text(x + 1, y + i * 8 + 1, line, shadow_col)
        pyxel.text(x, y + i * 8, line, col)


def format_number(n):
    """数値を読みやすい形式に（1000→1.0K, 1000000→1.0M）"""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}K"
    else:
        return str(int(n))
