"""Main game logic for 自動化帝国 (Phase 2)."""

import pyxel
import random

from src.constants import (
    WIDTH, HEIGHT, FONT_MAIN, FONT_SMALL,
    C_BLACK, C_NAVY, C_DGREEN, C_BROWN, C_DGRAY, C_GRAY, C_WHITE,
    C_RED, C_YELLOW, C_GREEN, C_SKYBLUE, C_LAVENDER, C_PINK, C_ORANGE, C_PEACH,
    REP_RANKS, STARTERS, RANDOM_NAMES,
    ALL_JOBS, EQUIPMENTS, MISHAPS, NAVIKO_MISHAP, NAVIKO_SUCCESS,
    AI_WEAKNESS, AI_STRENGTH,
    NAVIKO_OVERLOAD, NAVIKO_DEFRAG, NAVIKO_IDLE,
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
        self.rep_rank = 0  # index into REP_RANKS
        self.agents = []
        self.owned_equip = []  # list of equipment names

        # Job state
        self.available_jobs = []  # jobs shown on board this turn
        self.selected_job = None  # index into available_jobs
        self.current_job = None  # the job dict being executed

        # Turn result state
        self.turn_log = []
        self.turn_earned = 0
        self.mishap_event = None  # current mishap dict or None

        # UI state
        self.select_idx = 0
        self.naming_name = ""
        self.naviko_msg = ""
        self.job_scroll = 0  # scroll offset for job board
        self.equip_scroll = 0  # scroll offset for equip shop

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
        elif s == "mishap":
            # Mishap event screen - just acknowledge
            self.buttons["ok"] = Button(40, 268, 160, 36, "了解…")
        elif s == "ai_detail":
            self.buttons["defrag"] = Button(40, 236, 160, 32, "デフラグ")
            self.buttons["back"] = Button(40, 276, 160, 36, "戻る")
        elif s == "job_board":
            self._refresh_job_board()
            # Job buttons are created in _refresh_job_board
            self.buttons["back"] = Button(8, 276, 100, 36, "戻る")
        elif s == "equip_shop":
            self.equip_scroll = 0
            self.buttons["back"] = Button(8, 276, 100, 36, "戻る")

    def _refresh_job_board(self):
        """Generate available jobs based on reputation rank."""
        self.available_jobs = []
        for job in ALL_JOBS:
            if job["rank"] <= self.rep_rank:
                self.available_jobs.append(job)
        self.selected_job = None
        self.job_scroll = 0
        # Create job slot buttons (max 4 visible)
        for i in range(min(len(self.available_jobs), 4)):
            self.buttons[f"job{i}"] = Button(16, 44 + i * 54, 208, 48, "")

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
            self.current_job = None
            self.naviko_msg = (
                f"{self.naming_name}を雇った！\n"
                "まずは案件をこなそう。"
            )
            self.change_scene("office")

    def update_office(self):
        if self.buttons["next"].clicked():
            self._do_turn()
            return
        if self.buttons["ai"].clicked():
            self.change_scene("ai_detail")
            return
        if self.buttons["jobs"].clicked():
            self.change_scene("job_board")
            return
        if self.buttons["equip"].clicked():
            self.change_scene("equip_shop")
            return

    def update_result(self):
        if self.buttons["cont"].clicked():
            self.change_scene("office")

    def update_mishap(self):
        if self.buttons["ok"].clicked():
            self.change_scene("office")

    def update_ai_detail(self):
        if self.buttons["defrag"].clicked():
            self._do_defrag()
            return
        if self.buttons["back"].clicked():
            self.change_scene("office")

    def update_job_board(self):
        if self.buttons["back"].clicked():
            self.change_scene("office")
            return
        # Check job slot clicks
        visible_count = min(len(self.available_jobs) - self.job_scroll, 4)
        for i in range(visible_count):
            key = f"job{i}"
            if key in self.buttons and self.buttons[key].clicked():
                job_idx = self.job_scroll + i
                if self.selected_job == job_idx:
                    # Double tap = accept job
                    self.current_job = self.available_jobs[job_idx]
                    a = self.agents[0]
                    a["status"] = f"{self.current_job['name']}"
                    self.naviko_msg = (
                        f"「{self.current_job['name']}」を\n"
                        "受注した！「進む」で実行。"
                    )
                    self.change_scene("office")
                else:
                    self.selected_job = job_idx
                return

    def update_equip_shop(self):
        if self.buttons["back"].clicked():
            self.change_scene("office")
            return
        # Check equip slot clicks
        visible = self._visible_equips()
        for i, eq in enumerate(visible):
            key = f"eq{i}"
            if key in self.buttons and self.buttons[key].clicked():
                if eq["name"] not in self.owned_equip and self.coins >= eq["cost"]:
                    self.coins -= eq["cost"]
                    self.owned_equip.append(eq["name"])
                    self.naviko_msg = (
                        f"「{eq['name']}」を購入！\n"
                        f"{eq['desc']}"
                    )
                    self.change_scene("office")
                return

    def _visible_equips(self):
        """Get visible equipment list and create buttons."""
        visible = []
        for i, eq in enumerate(EQUIPMENTS):
            if i < self.equip_scroll:
                continue
            if len(visible) >= 4:
                break
            visible.append(eq)
        # Recreate buttons (keep back)
        back_btn = self.buttons.get("back")
        self.buttons = {}
        if back_btn:
            self.buttons["back"] = back_btn
        for i, eq in enumerate(visible):
            self.buttons[f"eq{i}"] = Button(16, 44 + i * 54, 208, 48, "")
        return visible

    # ── Turn logic ──

    def _do_defrag(self):
        """Defrag: skip 1 turn, reset load to 0."""
        a = self.agents[0]
        yr, mo, wk = self._week_to_date(self.week)

        a["fatigue"] = 0
        a["status"] = "デフラグ完了"

        self.turn_log = [
            f"{yr}年目 {mo}月 第{wk}週",
            "",
            f"{a['name']}を",
            "デフラグ実行中…",
            "",
            "負荷をリセットしました。",
            "",
            "（このターンは副業なし）",
        ]

        self.naviko_msg = random.choice(NAVIKO_DEFRAG)
        self.week += 1
        self.mishap_event = None
        self.change_scene("result")

    def _do_turn(self):
        a = self.agents[0]
        yr, mo, wk = self._week_to_date(self.week)

        job = self.current_job
        if job is None:
            # No job selected - idle week (chat with AI, no earnings)
            a["fatigue"] = max(0, a["fatigue"] - 1)
            a["status"] = "サボり"

            idle_msgs = [
                "あなたがYouTube見てたら\n1週間過ぎてた。",
                "あなたがSNS巡回してたら\n1週間溶けた。",
                "AIは暇すぎて\n自主学習を始めた。",
                "あなたが「あとでやる」\nと言って1週間経過。",
                "AIは指示待ちで\nずっとスリープしてた。",
            ]

            self.turn_log = [
                f"{yr}年目 {mo}月 第{wk}週",
                "",
                f"{a['name']}は",
                random.choice(idle_msgs),
                "",
                "収益: 0G",
                "",
                "（負荷が少し下がった）",
            ]

            self.naviko_msg = random.choice(NAVIKO_IDLE)
            self.week += 1
            self.mishap_event = None
            self.change_scene("result")
            return

        # Calculate earnings
        base_pay = job["pay"]
        pay_variance = random.randint(-20, 30)
        earned = base_pay + pay_variance

        # Stat bonus
        stat_name = job.get("stat")
        stat_val = 0
        if stat_name and stat_name in a["stats"]:
            stat_val = a["stats"][stat_name]
            # Bonus for high stat
            if stat_val >= job.get("threshold", 0):
                earned = int(earned * (1.0 + stat_val * 0.05))

        # Equipment bonus
        equip_bonus = self._calc_equip_bonus(stat_name)
        earned = int(earned * (1.0 + equip_bonus / 100.0))

        # Strength bonus (適性)
        agent_strength = AI_STRENGTH.get(a["id"])
        is_strong = (stat_name and agent_strength == stat_name)
        if is_strong:
            earned = int(earned * 1.3)

        # Check for mishap (やらかし)
        mishap_chance = self._calc_mishap_chance(a, job)
        mishap = None
        if random.random() < mishap_chance:
            mishap = self._pick_mishap(a)

        if mishap:
            # Mishap happened!
            cost = int(earned * mishap["cost_rate"])
            earned = earned - cost
            if earned < 0:
                earned = 0

            # Rep change from mishap
            rep_change = mishap.get("rep", 0)
            self.rep_rank = max(0, min(len(REP_RANKS) - 1, self.rep_rank + rep_change))

            self.coins += earned
            a["exp"] += 5  # less exp on mishap
            fat_add = 1 if self._has_equip("fatigue_reduce") else 2
            a["fatigue"] = min(10, a["fatigue"] + fat_add)
            a["status"] = "やらかし…"

            self.turn_log = [
                f"{yr}年目 {mo}月 第{wk}週",
                "",
                f"{a['name']}が",
                f"「{job['name']}」を実行…",
                "",
                "!! やらかし発生 !!",
                "",
            ]
            if earned > 0:
                self.turn_log.append(f"+{earned}G（減額…）")
            else:
                self.turn_log.append("収益ゼロ…")

            self.mishap_event = mishap
            self.naviko_msg = random.choice(NAVIKO_MISHAP)

            self.week += 1
            self._check_levelup(a)
            self.change_scene("result")
            return

        # Success path
        # Determine result quality
        quality = "成功"
        if stat_val >= 7 and random.random() < 0.3:
            quality = "大成功"
            earned = int(earned * 1.5)
            self.rep_rank = min(len(REP_RANKS) - 1, self.rep_rank + 1)
        elif stat_name and stat_val < job.get("threshold", 0):
            quality = "微妙"
            earned = int(earned * 0.6)

        self.coins += earned
        a["exp"] += 15 if is_strong else 10
        # Memory expansion: 50% chance to skip fatigue gain
        if self._has_equip("fatigue_reduce") and random.random() < 0.5:
            pass  # no fatigue gain this turn
        else:
            a["fatigue"] = min(10, a["fatigue"] + 1)
        a["status"] = "作業完了"

        self.turn_log = [
            f"{yr}年目 {mo}月 第{wk}週",
            "",
            f"{a['name']}が",
            f"「{job['name']}」を実行！",
            "",
        ]

        if quality == "大成功":
            self.turn_log.append(f"★★ 大成功！ +{earned}G")
            self.naviko_msg = "やるじゃん！大成功！"
        elif quality == "微妙":
            self.turn_log.append(f"+{earned}G（微妙…）")
            self.naviko_msg = "うーん、微妙だね。\nスキル上げた方がいいかも。"
        else:
            self.turn_log.append(f"+{earned}G")
            self.naviko_msg = random.choice(NAVIKO_SUCCESS)

        # Level up check
        self._check_levelup(a)

        # Monthly report
        if self.week % 4 == 0:
            self.naviko_msg = (
                f"{mo}月終了！\n"
                f"所持: {self.coins}G  評判:{REP_RANKS[self.rep_rank]}"
            )

        # Overload warning
        if a["fatigue"] >= 6:
            self.turn_log.append("")
            self.turn_log.append("⚠ 負荷が高い…")
            self.naviko_msg = random.choice(NAVIKO_OVERLOAD)

        self.week += 1
        self.mishap_event = None
        self.change_scene("result")

    def _calc_equip_bonus(self, stat_name):
        """Calculate equipment bonus percentage for a given stat."""
        bonus = 0
        for eq in EQUIPMENTS:
            if eq["name"] in self.owned_equip:
                if eq["effect"] == "all_bonus":
                    bonus += eq["bonus"]
                elif eq["effect"] == "bonus" and eq["stat"] == stat_name:
                    bonus += eq["bonus"]
        return bonus

    def _has_equip(self, effect_type):
        """Check if player owns equipment with given effect type."""
        for eq in EQUIPMENTS:
            if eq["effect"] == effect_type and eq["name"] in self.owned_equip:
                return True
        return False

    def _calc_mishap_chance(self, agent, job):
        """Calculate mishap probability."""
        base = 0.12
        # Weakness penalty
        stat_name = job.get("stat")
        weaknesses = AI_WEAKNESS.get(agent["id"], [])
        if stat_name and stat_name in weaknesses:
            base += 0.15
        # Accuracy reduces mishap
        accuracy = agent["stats"].get("正確", 0)
        base -= accuracy * 0.01
        # Fatigue increases mishap
        base += agent["fatigue"] * 0.02
        # Level reduces mishap
        base -= agent["level"] * 0.01
        # Cooling system reduces mishap
        if self._has_equip("mishap_reduce"):
            base -= 0.05
        return max(0.03, min(0.5, base))

    def _pick_mishap(self, agent):
        """Pick a random mishap for this agent."""
        pool = list(MISHAPS.get(agent["id"], []))
        pool += MISHAPS.get(None, [])
        return random.choice(pool)

    def _check_levelup(self, agent):
        """Check and apply level up."""
        needed = agent["level"] * 50
        if agent["exp"] >= needed:
            agent["exp"] = 0
            agent["level"] += 1
            # Stat growth on level up
            strength_stat = AI_STRENGTH.get(agent["id"])
            for stat in agent["stats"]:
                growth = random.randint(0, 1)
                if stat == strength_stat:
                    growth += 1
                agent["stats"][stat] = min(10, agent["stats"][stat] + growth)
            self.turn_log.append("")
            self.turn_log.append(f"★ Lv.{agent['level']}にアップ！")

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
        text_centered(300, "v0.2 - Phase 2", C_DGRAY, self.font_s)

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

        # Current job indicator
        if self.current_job:
            pyxel.text(8, 148, f"受注中: {self.current_job['name']}", C_GREEN, self.font_s)
        else:
            pyxel.text(8, 148, "案件未選択", C_DGRAY, self.font_s)

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

        if self.mishap_event:
            text_centered(10, "!! やらかし発生 !!", C_RED, self.font)
        else:
            text_centered(10, "今週の結果", C_YELLOW, self.font)

        y = 50
        for line in self.turn_log:
            if line == "":
                y += 6
                continue
            if "やらかし" in line:
                col = C_RED
            elif line.startswith("+") or "大成功" in line:
                col = C_GREEN
            elif line.startswith("★"):
                col = C_YELLOW
            elif "微妙" in line or "減額" in line or "ゼロ" in line:
                col = C_ORANGE
            elif "⚠" in line:
                col = C_ORANGE
            else:
                col = C_WHITE
            text_centered(y, line, col, self.font_s)
            y += 18

        # Show mishap detail
        if self.mishap_event:
            y += 4
            pyxel.rect(16, y, 208, 60, C_NAVY)
            pyxel.rectb(16, y, 208, 60, C_RED)
            for i, line in enumerate(self.mishap_event["text"].split("\n")):
                pyxel.text(24, y + 8 + i * 14, line, C_PINK, self.font_s)
            y += 66

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

        # Load (負荷)
        pyxel.text(24, sy, "負荷", C_GRAY, self.font_s)
        pyxel.rect(72, sy + 1, 100, 10, C_DGRAY)
        fat_w = min(a["fatigue"] * 10, 100)
        fat_col = C_RED if a["fatigue"] >= 6 else C_ORANGE if a["fatigue"] >= 3 else C_GREEN
        pyxel.rect(72, sy + 1, fat_w, 10, fat_col)
        if a["fatigue"] >= 6:
            pyxel.text(180, sy, "危険", C_RED, self.font_s)
        sy += 20

        text_centered(sy + 6, f"状態: {a['status']}", C_WHITE, self.font_s)

        # Defrag button
        defrag_col = C_DGREEN if a["fatigue"] >= 3 else C_DGRAY
        defrag_txt_col = C_WHITE if a["fatigue"] >= 3 else C_GRAY
        self.buttons["defrag"].draw(self.font_s, defrag_col, defrag_txt_col, C_GREEN if a["fatigue"] >= 3 else C_GRAY)

        self.buttons["back"].draw(self.font, C_DGRAY, C_WHITE, C_GRAY)

    def draw_job_board(self):
        pyxel.cls(C_BLACK)
        text_centered(10, "案件ボード", C_YELLOW, self.font)
        pyxel.text(8, 30, "タップで選択→もう一度タップで受注", C_GRAY, self.font_s)

        if not self.available_jobs:
            text_centered(140, "案件がありません", C_DGRAY, self.font_s)
        else:
            visible_start = self.job_scroll
            visible_end = min(visible_start + 4, len(self.available_jobs))
            for vi, ji in enumerate(range(visible_start, visible_end)):
                job = self.available_jobs[ji]
                y = 44 + vi * 54
                is_selected = (self.selected_job == ji)
                bg_col = C_DGREEN if is_selected else C_NAVY
                border_col = C_GREEN if is_selected else C_GRAY

                draw_panel(16, y, 208, 48, bg_col, border_col)
                pyxel.text(24, y + 6, job["name"], C_WHITE, self.font_s)
                pyxel.text(24, y + 22, f"報酬:{job['pay']}G  難度:{job['diff']}", C_GRAY, self.font_s)

                # Show stat requirement
                if job.get("stat"):
                    req_text = f"要:{job['stat']}{job['threshold']}"
                    pyxel.text(150, y + 6, req_text, C_SKYBLUE, self.font_s)

                # Show if currently assigned
                if self.current_job and self.current_job["name"] == job["name"]:
                    pyxel.text(150, y + 32, "受注中", C_GREEN, self.font_s)

        # Scroll indicators
        if self.job_scroll > 0:
            text_centered(38, "▲", C_GRAY, self.font_s)
        if self.job_scroll + 4 < len(self.available_jobs):
            text_centered(264, "▼", C_GRAY, self.font_s)

        self.buttons["back"].draw(self.font_s, C_DGRAY, C_WHITE, C_GRAY)

    def draw_equip_shop(self):
        pyxel.cls(C_BLACK)
        text_centered(10, "設備ショップ", C_YELLOW, self.font)
        pyxel.text(8, 28, f"所持金: {self.coins}G", C_GREEN, self.font_s)

        visible = self._visible_equips()
        if not visible:
            text_centered(140, "設備がありません", C_DGRAY, self.font_s)
        else:
            for i, eq in enumerate(visible):
                y = 44 + i * 54
                owned = eq["name"] in self.owned_equip
                can_buy = self.coins >= eq["cost"] and not owned

                if owned:
                    bg_col = C_DGRAY
                    border_col = C_GRAY
                elif can_buy:
                    bg_col = C_NAVY
                    border_col = C_GREEN
                else:
                    bg_col = C_NAVY
                    border_col = C_DGRAY

                draw_panel(16, y, 208, 48, bg_col, border_col)
                pyxel.text(24, y + 6, eq["name"], C_WHITE, self.font_s)
                pyxel.text(24, y + 22, eq["desc"], C_GRAY, self.font_s)

                if owned:
                    pyxel.text(160, y + 6, "購入済", C_GRAY, self.font_s)
                else:
                    cost_col = C_GREEN if can_buy else C_RED
                    pyxel.text(150, y + 6, f"{eq['cost']}G", cost_col, self.font_s)

        self.buttons["back"].draw(self.font_s, C_DGRAY, C_WHITE, C_GRAY)

    # ── Avatar drawing ──

    def _draw_avatar_small(self, agent_id, x, y, col):
        """Draw a small ~24x24 avatar at top-left (x, y)."""
        if agent_id == "poem":
            pyxel.circ(x + 12, y + 14, 12, col)
            pyxel.pset(x + 8, y + 11, C_WHITE)
            pyxel.pset(x + 16, y + 11, C_WHITE)
            pyxel.rect(x + 4, y, 16, 6, col)
        elif agent_id == "bugmaru":
            pyxel.rect(x, y + 2, 24, 22, col)
            pyxel.rectb(x + 3, y + 9, 8, 6, C_WHITE)
            pyxel.rectb(x + 13, y + 9, 8, 6, C_WHITE)
            pyxel.line(x + 11, y + 11, x + 13, y + 11, C_WHITE)
        else:
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
