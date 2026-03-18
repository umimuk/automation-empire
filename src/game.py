"""Main game logic for 自動化帝国 (Phase 1)."""

import pyxel
import random

from src.constants import (
    WIDTH, HEIGHT, FONT_MAIN, FONT_SMALL,
    C_BLACK, C_NAVY, C_DGREEN, C_BROWN, C_DGRAY, C_GRAY, C_WHITE,
    C_YELLOW, C_GREEN, C_SKYBLUE, C_LAVENDER, C_PINK,
    REP_RANKS, STARTERS, RANDOM_NAMES,
)
from src.ui import Button, text_centered, draw_panel


class Game:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="自動化帝国", quit_key=pyxel.KEY_NONE)
        pyxel.mouse(True)

        # Fonts
        self.font = pyxel.Font(FONT_MAIN)
        self.font_s = pyxel.Font(FONT_SMALL)

        # Scene
        self.scene = "title"
        self.buttons = {}

        # Game state
        self.week = 0
        self.coins = 0
        self.rep_rank = 0
        self.agents = []

        # UI state
        self.select_idx = 0
        self.naming_name = ""
        self.turn_log = []
        self.naviko_msg = ""

        self._setup_scene()
        pyxel.run(self.update, self.draw)

    # ── Scene management ──

    def change_scene(self, scene):
        self.scene = scene
        self._setup_scene()

    def _setup_scene(self):
        self.buttons = {}
        s = self.scene
        if s == "select":
            for i in range(3):
                self.buttons[f"c{i}"] = Button(20, 50 + i * 85, 200, 75, "")
        elif s == "naming":
            self.buttons["rand"] = Button(40, 224, 160, 36, "ランダム生成")
            self.buttons["ok"] = Button(40, 272, 160, 36, "決定")
        elif s == "office":
            bw, bh = 108, 44
            self.buttons["jobs"] = Button(8, 216, bw, bh, "案件ボード")
            self.buttons["ai"] = Button(124, 216, bw, bh, "AI管理")
            self.buttons["equip"] = Button(8, 268, bw, bh, "設備")
            self.buttons["next"] = Button(124, 268, bw, bh, "進む")
        elif s == "result":
            self.buttons["cont"] = Button(40, 272, 160, 36, "次へ")
        elif s in ("ai_detail", "job_board"):
            self.buttons["back"] = Button(40, 276, 160, 36, "戻る")

    # ── Update dispatch ──

    def update(self):
        fn = getattr(self, f"update_{self.scene}", None)
        if fn:
            fn()

    def update_title(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.change_scene("select")

    def update_select(self):
        for i in range(3):
            if self.buttons[f"c{i}"].clicked():
                self.select_idx = i
                self.naming_name = STARTERS[i]["name"]
                self.change_scene("naming")
                return

    def update_naming(self):
        if self.buttons["rand"].clicked():
            names = [n for n in RANDOM_NAMES if n != self.naming_name]
            self.naming_name = random.choice(names)
        elif self.buttons["ok"].clicked():
            starter = STARTERS[self.select_idx]
            self.agents = [{
                "id": starter["id"],
                "name": self.naming_name,
                "type_label": starter["type_label"],
                "color": starter["color"],
                "level": 1,
                "exp": 0,
                "stats": dict(starter["stats"]),
                "fatigue": 0,
                "status": "待機中",
            }]
            self.week = 1
            self.coins = 1000
            self.rep_rank = 0
            self.naviko_msg = (
                f"{self.naming_name}を雇った！\n"
                "まずは案件をこなそう。"
            )
            self.change_scene("office")

    def update_office(self):
        if self.buttons["next"].clicked():
            self._do_turn()
        elif self.buttons["ai"].clicked():
            self.change_scene("ai_detail")
        elif self.buttons["jobs"].clicked():
            self.change_scene("job_board")
        # equip: Phase 2+

    def update_result(self):
        if self.buttons["cont"].clicked():
            self.change_scene("office")

    def update_ai_detail(self):
        if self.buttons["back"].clicked():
            self.change_scene("office")

    def update_job_board(self):
        if self.buttons["back"].clicked():
            self.change_scene("office")

    # ── Turn logic ──

    def _do_turn(self):
        a = self.agents[0]
        yr, mo, wk = self._week_to_date(self.week)

        # Simple placeholder: data entry job
        earned = random.randint(80, 200)
        self.coins += earned
        a["exp"] += 10
        a["status"] = "作業中"

        self.turn_log = [
            f"{yr}年目 {mo}月 第{wk}週",
            "",
            f"{a['name']}が",
            "データ入力をこなした！",
            "",
            f"+{earned} コイン",
        ]

        # Level up check
        if a["exp"] >= a["level"] * 50:
            a["exp"] = 0
            a["level"] += 1
            self.turn_log.append("")
            self.turn_log.append(f"★ Lv.{a['level']}にアップ！")

        # Naviko message
        if self.week % 4 == 0:
            self.naviko_msg = f"{mo}月終了！\n所持: {self.coins}G"
        else:
            msgs = [
                "順調だね。", "まあまあかな。",
                "この調子！", "悪くないよ。", "頑張ってるね。",
            ]
            self.naviko_msg = random.choice(msgs)

        self.week += 1
        self.change_scene("result")

    def _week_to_date(self, w):
        yr = (w - 1) // 48 + 1
        mo = ((w - 1) % 48) // 4 + 1
        wk = (w - 1) % 4 + 1
        return yr, mo, wk

    # ── Draw dispatch ──

    def draw(self):
        pyxel.cls(C_NAVY)
        fn = getattr(self, f"draw_{self.scene}", None)
        if fn:
            fn()

    def draw_title(self):
        pyxel.cls(C_BLACK)
        text_centered(100, "自動化帝国", C_YELLOW, self.font)
        text_centered(130, "AI副業経営シミュレーション", C_WHITE, self.font_s)
        if pyxel.frame_count % 60 < 40:
            text_centered(230, "タップしてスタート", C_GRAY, self.font_s)
        text_centered(300, "v0.1 - Phase 1", C_DGRAY, self.font_s)

    def draw_select(self):
        pyxel.cls(C_BLACK)
        text_centered(15, "パートナーを選べ", C_YELLOW, self.font)
        text_centered(32, "タップして選択", C_GRAY, self.font_s)

        for i, st in enumerate(STARTERS):
            b = self.buttons[f"c{i}"]
            pyxel.rect(b.x, b.y, b.w, b.h, C_NAVY)
            pyxel.rectb(b.x, b.y, b.w, b.h, st["color"])

            # Avatar
            ax, ay = b.x + 14, b.y + 14
            self._draw_avatar_small(st["id"], ax, ay, st["color"])

            # Text
            tx = b.x + 52
            pyxel.text(tx, b.y + 8, st["name"], C_WHITE, self.font)
            pyxel.text(tx, b.y + 26, st["type_label"], st["color"], self.font_s)
            for j, line in enumerate(st["desc"].split("\n")):
                pyxel.text(tx, b.y + 44 + j * 14, line, C_GRAY, self.font_s)

    def draw_naming(self):
        pyxel.cls(C_BLACK)
        st = STARTERS[self.select_idx]

        text_centered(15, "名前をつけよう", C_YELLOW, self.font)
        self._draw_avatar_large(st["id"], 120, 80, st["color"])
        text_centered(118, st["type_label"], st["color"], self.font_s)

        # Name display panel
        draw_panel(30, 155, 180, 36, C_NAVY, C_GRAY)
        text_centered(163, self.naming_name, C_WHITE, self.font)

        # Buttons
        self.buttons["rand"].draw(self.font_s, C_DGRAY, C_WHITE, C_GRAY)
        self.buttons["ok"].draw(self.font, C_DGREEN, C_WHITE, C_GREEN)

    def draw_office(self):
        # Status bar
        pyxel.rect(0, 0, WIDTH, 20, C_BLACK)
        pyxel.text(4, 5, f"{self.coins}G", C_YELLOW, self.font_s)
        rank = REP_RANKS[self.rep_rank]
        pyxel.text(90, 5, f"評判:{rank}", C_WHITE, self.font_s)
        if self.week > 0:
            yr, mo, _ = self._week_to_date(self.week)
            pyxel.text(175, 5, f"{yr}年{mo}月", C_GRAY, self.font_s)

        # Office area
        pyxel.rect(0, 20, WIDTH, 140, C_NAVY)
        # Floor line
        pyxel.line(0, 145, WIDTH, 145, C_DGRAY)
        # Desk
        pyxel.rect(60, 125, 120, 16, C_BROWN)
        # Monitor
        pyxel.rect(98, 105, 44, 20, C_DGRAY)
        pyxel.rect(102, 108, 36, 14, C_SKYBLUE)

        # Agent at desk
        if self.agents:
            a = self.agents[0]
            bob = -2 if (pyxel.frame_count // 20) % 2 else 0
            self._draw_avatar_small(a["id"], 108, 80 + bob, a["color"])

        # Naviko message area
        pyxel.rect(0, 160, WIDTH, 48, C_BLACK)
        pyxel.rectb(0, 160, WIDTH, 48, C_DGRAY)
        # Naviko icon
        pyxel.circ(16, 180, 10, C_LAVENDER)
        pyxel.text(10, 176, "ナ", C_WHITE, self.font_s)
        # Message
        for i, line in enumerate(self.naviko_msg.split("\n")):
            pyxel.text(34, 168 + i * 14, line, C_WHITE, self.font_s)

        # Bottom buttons
        for key in ("jobs", "ai", "equip"):
            self.buttons[key].draw(self.font_s, C_DGRAY, C_WHITE, C_GRAY)
        self.buttons["next"].draw(self.font_s, C_DGREEN, C_WHITE, C_GREEN)

    def draw_result(self):
        pyxel.cls(C_BLACK)
        text_centered(20, "今週の結果", C_YELLOW, self.font)

        y = 70
        for line in self.turn_log:
            if line == "":
                y += 8
                continue
            if line.startswith("+"):
                col = C_GREEN
            elif line.startswith("★"):
                col = C_YELLOW
            else:
                col = C_WHITE
            text_centered(y, line, col, self.font_s)
            y += 22

        self.buttons["cont"].draw(self.font, C_DGRAY, C_WHITE, C_GRAY)

    def draw_ai_detail(self):
        pyxel.cls(C_BLACK)
        if not self.agents:
            return
        a = self.agents[0]

        text_centered(10, "AI管理", C_YELLOW, self.font)
        self._draw_avatar_large(a["id"], 120, 56, a["color"])
        text_centered(88, f"{a['name']}  Lv.{a['level']}", C_WHITE, self.font)
        text_centered(106, a["type_label"], a["color"], self.font_s)

        # Stat bars
        sy = 130
        for name in ("創造", "技術", "営業", "正確", "体力"):
            val = a["stats"].get(name, 0)
            pyxel.text(24, sy, name, C_GRAY, self.font_s)
            pyxel.rect(72, sy + 1, 100, 10, C_DGRAY)
            bar_w = min(val * 10, 100)
            col = C_GREEN if val >= 5 else C_SKYBLUE
            pyxel.rect(72, sy + 1, bar_w, 10, col)
            pyxel.text(180, sy, str(val), C_WHITE, self.font_s)
            sy += 20

        text_centered(sy + 10, f"状態: {a['status']}", C_WHITE, self.font_s)
        self.buttons["back"].draw(self.font, C_DGRAY, C_WHITE, C_GRAY)

    def draw_job_board(self):
        pyxel.cls(C_BLACK)
        text_centered(10, "案件ボード", C_YELLOW, self.font)

        jobs = [
            ("データ入力", 100, "★"),
            ("アンケート代筆", 120, "★"),
            ("リサーチ代行", 150, "★☆"),
        ]
        for i, (name, pay, diff) in enumerate(jobs):
            y = 50 + i * 60
            draw_panel(20, y, 200, 48, C_NAVY, C_GRAY)
            pyxel.text(30, y + 8, name, C_WHITE, self.font_s)
            pyxel.text(30, y + 26, f"報酬:{pay}G  難度:{diff}", C_GRAY, self.font_s)

        text_centered(240, "※フェーズ2で実装", C_DGRAY, self.font_s)
        self.buttons["back"].draw(self.font, C_DGRAY, C_WHITE, C_GRAY)

    # ── Avatar drawing ──

    def _draw_avatar_small(self, agent_id, x, y, col):
        """Draw a small ~24x24 avatar at top-left (x, y)."""
        if agent_id == "poem":
            # Round shape + beret
            pyxel.circ(x + 12, y + 14, 12, col)
            pyxel.pset(x + 8, y + 11, C_WHITE)
            pyxel.pset(x + 16, y + 11, C_WHITE)
            pyxel.rect(x + 4, y, 16, 6, col)
        elif agent_id == "bugmaru":
            # Square + glasses
            pyxel.rect(x, y + 2, 24, 22, col)
            pyxel.rectb(x + 3, y + 9, 8, 6, C_WHITE)
            pyxel.rectb(x + 13, y + 9, 8, 6, C_WHITE)
            pyxel.line(x + 11, y + 11, x + 13, y + 11, C_WHITE)
        else:
            # Triangle (sharp/business)
            pyxel.tri(x + 12, y, x, y + 24, x + 24, y + 24, col)
            pyxel.pset(x + 9, y + 12, C_WHITE)
            pyxel.pset(x + 15, y + 12, C_WHITE)

    def _draw_avatar_large(self, agent_id, cx, cy, col):
        """Draw a large avatar centered at (cx, cy)."""
        if agent_id == "poem":
            pyxel.circ(cx, cy, 22, col)
            pyxel.pset(cx - 7, cy - 5, C_WHITE)
            pyxel.pset(cx + 7, cy - 5, C_WHITE)
            pyxel.line(cx - 4, cy + 6, cx + 4, cy + 6, C_WHITE)
            pyxel.rect(cx - 14, cy - 24, 28, 8, col)
        elif agent_id == "bugmaru":
            pyxel.rect(cx - 22, cy - 20, 44, 44, col)
            pyxel.rectb(cx - 14, cy - 6, 12, 10, C_WHITE)
            pyxel.rectb(cx + 2, cy - 6, 12, 10, C_WHITE)
            pyxel.line(cx - 2, cy - 2, cx + 2, cy - 2, C_WHITE)
            pyxel.line(cx - 6, cy + 10, cx + 6, cy + 10, C_WHITE)
        else:
            pyxel.tri(cx, cy - 26, cx - 22, cy + 22, cx + 22, cy + 22, col)
            pyxel.pset(cx - 5, cy - 4, C_WHITE)
            pyxel.pset(cx + 5, cy - 4, C_WHITE)
            pyxel.line(cx - 6, cy + 6, cx + 6, cy + 6, C_WHITE)
