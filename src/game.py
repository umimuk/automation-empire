"""Main game logic for 自動化帝国 (Phase 5)."""

import pyxel
import random

import os

from src.constants import (
    WIDTH, HEIGHT, FONT_MAIN, FONT_SMALL,
    C_BLACK, C_NAVY, C_PURPLE, C_DGREEN, C_BROWN, C_DGRAY, C_GRAY, C_WHITE,
    C_RED, C_ORANGE, C_YELLOW, C_GREEN, C_SKYBLUE, C_LAVENDER, C_PINK, C_PEACH,
    REP_RANKS, STARTERS, RANDOM_NAMES,
    ALL_JOBS, EQUIPMENTS, MISHAPS, NAVIKO_MISHAP, NAVIKO_SUCCESS,
    AI_WEAKNESS, AI_STRENGTH,
    NAVIKO_OVERLOAD, NAVIKO_DEFRAG, NAVIKO_IDLE,
    OFFICE_LEVELS, TAX_EVENT_CHOICES, TAX_AGENT_FAILS,
    NAVIKO_MONTHLY_GOOD, NAVIKO_MONTHLY_BAD, NAVIKO_MONTHLY_GREAT,
    NAVIKO_MONTHLY_MISHAP0, NAVIKO_MONTHLY_MISHAP_FEW, NAVIKO_MONTHLY_MISHAP_MANY,
    NAVIKO_RANKUP, NAVIKO_TAX,
    SYNERGIES, TITLES, ENDINGS, GAME_LENGTH_WEEKS,
    NAVIKO_SYNERGY, NAVIKO_TITLE,
)

# Sprite sheet layout: each sprite 64x64, colkey=8 (red)
_SPRITE_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "sprites.png")
SPRITE_COLKEY = 0  # C_BLACK used as transparent color
SPRITE_SZ = 64  # sprite size in pixels
# agent_id -> (u, v) position in sprite sheet
SPRITE_UV = {
    "poem": (0, 0),
    "bugmaru": (64, 0),
    "hattari": (128, 0),
    "nabiko": (192, 0),
}
from src.ui import Button, text_centered, draw_panel


class Game:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="自動化帝国", quit_key=pyxel.KEY_NONE)
        pyxel.mouse(True)

        # Fonts
        self.font = pyxel.Font(FONT_MAIN)
        self.font_s = pyxel.Font(FONT_SMALL)

        # Load sprite sheet into image bank 0
        pyxel.images[0].load(0, 0, _SPRITE_FILE)

        # Scene
        self.scene = "title"
        self.buttons = {}

        # Game state
        self.week = 0
        self.coins = 0
        self.rep_rank = 0  # index into REP_RANKS
        self.agents = []
        self.owned_equip = []  # list of equipment names
        self.office_level = 0  # Phase 4: index into OFFICE_LEVELS

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

        # Phase 4: Monthly tracking
        self.month_earnings = 0
        self.month_mishaps = 0
        self.year_earnings = 0

        # Phase 4: Event queue
        self.pending_scenes = []
        self.prev_rep_rank = 0
        self.rankup_from = 0

        # Phase 4: Monthly report snapshot
        self.report_data = {}

        # Phase 4: Tax event
        self.tax_year_income = 0

        # Phase 5: Achievement tracking
        self.total_mishaps = 0
        self.consecutive_mishaps = 0
        self.consecutive_idles = 0
        self.completed_jobs = set()
        self.earned_titles = []
        self.active_synergies = []
        self.total_earnings = 0
        self._scene_comment = ""
        self.ending_data = None
        self.work_timer = 0

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
                self.buttons[f"c{i}"] = Button(20, 60 + i * 120, 230, 100, "")
        elif s == "naming":
            self.buttons["rand"] = Button(55, 340, 160, 40, "ランダム生成")
            self.buttons["ok"] = Button(55, 400, 160, 40, "決定")
        elif s == "office":
            bw, bh = 120, 50
            self.buttons["jobs"] = Button(12, 350, bw, bh, "案件ボード")
            self.buttons["ai"] = Button(138, 350, bw, bh, "AI管理")
            self.buttons["equip"] = Button(12, 410, bw, bh, "設備")
            self.buttons["next"] = Button(138, 410, bw, bh, "進む")
        elif s == "working":
            self.work_timer = 0
        elif s == "result":
            self.buttons["cont"] = Button(55, 420, 160, 40, "次へ")
        elif s == "mishap":
            for i in range(4):
                self.buttons[f"ch{i}"] = Button(16, 180 + i * 60, 238, 52, "")
        elif s == "ai_detail":
            self.buttons["defrag"] = Button(55, 380, 160, 36, "デフラグ")
            self.buttons["back"] = Button(55, 430, 160, 40, "戻る")
        elif s == "job_board":
            self._refresh_job_board()
            self.buttons["back"] = Button(12, 430, 110, 40, "戻る")
        elif s == "equip_shop":
            self.equip_scroll = 0
            self.buttons["back"] = Button(12, 430, 110, 40, "戻る")
            if self.office_level < len(OFFICE_LEVELS) - 1:
                self.buttons["office_up"] = Button(20, 46, 230, 54, "")
        elif s == "monthly_report":
            self.buttons["cont"] = Button(55, 420, 160, 40, "次へ")
            d = self.report_data
            mishaps = d.get("mishaps", 0)
            # やらかし回数に応じてナビ子セリフを分岐
            if mishaps == 0:
                self._scene_comment = random.choice(NAVIKO_MONTHLY_MISHAP0)
            elif mishaps <= 2:
                self._scene_comment = random.choice(NAVIKO_MONTHLY_MISHAP_FEW)
            else:
                self._scene_comment = random.choice(NAVIKO_MONTHLY_MISHAP_MANY)
        elif s == "rankup":
            self.buttons["cont"] = Button(55, 420, 160, 40, "次へ")
            self._scene_comment = random.choice(NAVIKO_RANKUP)
        elif s == "tax_event":
            for i in range(4):
                self.buttons[f"tax{i}"] = Button(16, 180 + i * 60, 238, 52, "")
            self._scene_comment = random.choice(NAVIKO_TAX)
        elif s == "ending":
            self.buttons["restart"] = Button(55, 430, 160, 40, "もう一度遊ぶ")
            self.ending_data = self._determine_ending()
            if self.total_mishaps == 0:
                earned_ids = {t["id"] for t in self.earned_titles}
                if "perfectionist" not in earned_ids:
                    for t in TITLES:
                        if t["id"] == "perfectionist":
                            self.earned_titles.append(t)
                            break

    def _refresh_job_board(self):
        """Generate available jobs based on reputation rank."""
        self.available_jobs = []
        for job in ALL_JOBS:
            if job["rank"] <= self.rep_rank:
                self.available_jobs.append(job)
        self.selected_job = None
        self.job_scroll = 0
        # Create job slot buttons (max 5 visible)
        for i in range(min(len(self.available_jobs), 5)):
            self.buttons[f"job{i}"] = Button(20, 54 + i * 66, 230, 58, "")

    # ── Scene transition helper ──

    def _next_scene(self):
        """Go to next pending event scene, or back to office."""
        if self.pending_scenes:
            scene = self.pending_scenes.pop(0)
            self.change_scene(scene)
        else:
            self.change_scene("office")

    # ── Post-turn event check ──

    def _check_post_turn_events(self):
        """Queue events after a turn (rank up, monthly report, tax)."""
        self.pending_scenes = []

        # Rank up check
        if self.rep_rank > self.prev_rep_rank:
            self.rankup_from = self.prev_rep_rank
            self.pending_scenes.append("rankup")
        self.prev_rep_rank = self.rep_rank

        # Monthly report (every 4 weeks)
        prev_week = self.week - 1  # the week that just completed
        if prev_week > 0 and prev_week % 4 == 0:
            yr, mo, _ = self._week_to_date(prev_week)
            self.report_data = {
                "month": mo,
                "year": yr,
                "earnings": self.month_earnings,
                "mishaps": self.month_mishaps,
                "rank": REP_RANKS[self.rep_rank],
                "level": self.agents[0]["level"] if self.agents else 1,
            }
            self.pending_scenes.append("monthly_report")
            # Reset monthly tracking
            self.month_earnings = 0
            self.month_mishaps = 0

        # Tax event (2月第1週 of year 2+)
        next_yr, next_mo, next_wk = self._week_to_date(self.week)
        if next_yr >= 2 and next_mo == 2 and next_wk == 1:
            self.tax_year_income = self.year_earnings
            self.year_earnings = 0
            self.pending_scenes.append("tax_event")

        # Phase 5: Game end (3 years = 144 weeks)
        if self.week > GAME_LENGTH_WEEKS:
            self.pending_scenes.append("ending")

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
            self.prev_rep_rank = 0
            self.current_job = None
            self.naviko_msg = (
                f"{self.naming_name}を雇った！\n"
                "まずは案件をこなそう。"
            )
            self.change_scene("office")

    def update_office(self):
        if self.buttons["next"].clicked():
            # Transition to working animation before processing turn
            self.change_scene("working")
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

    def update_working(self):
        """Working animation - auto-advance after ~90 frames (3 seconds)."""
        self.work_timer += 1
        if self.work_timer >= 90:
            if getattr(self, '_is_defragging', False):
                self._is_defragging = False
                self._do_defrag()
            else:
                self._do_turn()

    def update_result(self):
        if self.buttons["cont"].clicked():
            if self.mishap_event and self.mishap_event.get("choices"):
                self.change_scene("mishap")
            else:
                self._next_scene()

    def update_mishap(self):
        if not self.mishap_event:
            self._next_scene()
            return
        choices = self.mishap_event.get("choices", [])
        for i, choice in enumerate(choices):
            key = f"ch{i}"
            if key in self.buttons and self.buttons[key].clicked():
                self._apply_choice(choice)
                self.mishap_event = None
                self._next_scene()
                return

    def _apply_choice(self, choice):
        """Apply the effect of a mishap choice."""
        if choice.get("gamble", False):
            if random.random() < 0.5:
                # Gamble success
                cost = choice.get("cost", 0)
                rep = choice.get("rep", 0)
                fatigue = choice.get("fatigue", 0)
                result_text = choice.get("result_text", "")
            else:
                # Gamble fail - use separate fail values
                cost = choice.get("gamble_fail_cost", 0)
                rep = choice.get("gamble_fail_rep", 0)
                fatigue = choice.get("gamble_fail_fatigue", 0)
                result_text = choice.get("gamble_fail_text", "Failed.")
        else:
            cost = choice.get("cost", 0)
            rep = choice.get("rep", 0)
            fatigue = choice.get("fatigue", 0)
            result_text = choice.get("result_text", "")
        self.coins = max(0, self.coins + cost)
        self.rep_rank = max(0, min(len(REP_RANKS) - 1, self.rep_rank + rep))
        if self.agents and fatigue != 0:
            a = self.agents[0]
            a["fatigue"] = max(0, min(10, a["fatigue"] + fatigue))
        # Build result message with cost display
        if cost > 0:
            cost_text = f"（+{cost}G）"
        elif cost < 0:
            cost_text = f"（{cost}G）"
        else:
            cost_text = "（±0G）"
        self.naviko_msg = f"{result_text}\n{cost_text}"

    # Phase 4: New scene updates

    def update_monthly_report(self):
        if self.buttons["cont"].clicked():
            self._next_scene()

    def update_rankup(self):
        if self.buttons["cont"].clicked():
            self._next_scene()

    def update_tax_event(self):
        for i, tc in enumerate(TAX_EVENT_CHOICES):
            key = f"tax{i}"
            if key in self.buttons and self.buttons[key].clicked():
                self._apply_tax(tc)
                self._next_scene()
                return

    def _apply_tax(self, choice):
        """Apply tax event choice."""
        if choice.get("gamble", False):
            if random.random() < 0.5:
                # AI did well
                tax_rate = choice["tax_rate"]
                rep = choice.get("rep", 0)
                result_text = choice.get("result_text", "")
            else:
                # AI messed up
                tax_rate = choice.get("gamble_fail_tax_rate", 0.25)
                rep = choice.get("gamble_fail_rep", 0)
                # Use agent-specific fail text if available
                agent_id = self.agents[0]["id"] if self.agents else None
                result_text = TAX_AGENT_FAILS.get(agent_id, choice.get("gamble_fail_text", ""))
        else:
            tax_rate = choice["tax_rate"]
            rep = choice.get("rep", 0)
            result_text = choice.get("result_text", "")

        tax_amount = int(self.tax_year_income * tax_rate)
        self.coins = max(0, self.coins - tax_amount)
        self.rep_rank = max(0, min(len(REP_RANKS) - 1, self.rep_rank + rep))

        # Fatigue from doing it yourself
        fatigue = choice.get("fatigue", 0)
        if self.agents and fatigue != 0:
            a = self.agents[0]
            a["fatigue"] = max(0, min(10, a["fatigue"] + fatigue))

        self.naviko_msg = f"{result_text}\n（税金: -{tax_amount}G）"

    def update_ai_detail(self):
        if self.buttons["defrag"].clicked():
            self._is_defragging = True
            self.change_scene("working")
            return
        if self.buttons["back"].clicked():
            self.change_scene("office")

    def update_job_board(self):
        if self.buttons["back"].clicked():
            self.change_scene("office")
            return
        # Scroll handling
        if "scroll_up" in self.buttons and self.buttons["scroll_up"].clicked():
            if self.job_scroll > 0:
                self.job_scroll -= 1
            return
        if "scroll_down" in self.buttons and self.buttons["scroll_down"].clicked():
            if self.job_scroll + 4 < len(self.available_jobs):
                self.job_scroll += 1
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
        # Phase 4: Office upgrade
        if "office_up" in self.buttons and self.buttons["office_up"].clicked():
            if self.office_level < len(OFFICE_LEVELS) - 1:
                next_lv = OFFICE_LEVELS[self.office_level + 1]
                if self.coins >= next_lv["cost"]:
                    self.coins -= next_lv["cost"]
                    self.office_level += 1
                    cur = OFFICE_LEVELS[self.office_level]
                    self.naviko_msg = (
                        f"事務所を拡張！\n"
                        f"{cur['name']}に！ {cur['desc']}"
                    )
                    self.change_scene("office")
            return
        # Scroll handling
        if "scroll_up" in self.buttons and self.buttons["scroll_up"].clicked():
            if self.equip_scroll > 0:
                self.equip_scroll -= 1
            return
        if "scroll_down" in self.buttons and self.buttons["scroll_down"].clicked():
            if self.equip_scroll + 4 < len(EQUIPMENTS):
                self.equip_scroll += 1
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
        has_office_btn = self.office_level < len(OFFICE_LEVELS) - 1
        eq_y_start = 110 if has_office_btn else 44
        max_visible = 3 if has_office_btn else 4

        visible = []
        for i, eq in enumerate(EQUIPMENTS):
            if i < self.equip_scroll:
                continue
            if len(visible) >= max_visible:
                break
            visible.append(eq)
        # Recreate buttons (keep back + office_up)
        back_btn = self.buttons.get("back")
        office_btn = self.buttons.get("office_up")
        self.buttons = {}
        if back_btn:
            self.buttons["back"] = back_btn
        if office_btn:
            self.buttons["office_up"] = office_btn
        for i, eq in enumerate(visible):
            self.buttons[f"eq{i}"] = Button(16, eq_y_start + i * 64, 208, 56, "")
        return visible

    # ── Turn logic ──

    def _do_defrag(self):
        """Defrag: skip 1 turn, reset load to 0."""
        a = self.agents[0]
        yr, mo, wk = self._week_to_date(self.week)

        # Phase 4: Office fatigue bonus
        extra = 0
        if OFFICE_LEVELS[self.office_level].get("desc", "").find("負荷回復") >= 0:
            extra = 1  # bonus recovery text in defrag

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
        # Phase 5: Defrag resets streaks
        self.consecutive_mishaps = 0
        self.consecutive_idles = 0
        self._phase5_post_turn()
        self._check_post_turn_events()
        self.change_scene("result")

    def _do_turn(self):
        a = self.agents[0]
        yr, mo, wk = self._week_to_date(self.week)
        self.prev_rep_rank = self.rep_rank  # Track for rank up check

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
                random.choice(idle_msgs),
                "",
                "収益: 0G",
                "",
                "（負荷が少し下がった）",
            ]

            self.naviko_msg = random.choice(NAVIKO_IDLE)
            self.week += 1
            self.mishap_event = None
            # Phase 5: Track idle streaks
            self.consecutive_idles += 1
            self.consecutive_mishaps = 0
            self._phase5_post_turn()
            self._check_post_turn_events()
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

        # Phase 4: Office bonus
        office_bonus = OFFICE_LEVELS[self.office_level]["bonus"]
        if office_bonus > 0:
            earned = int(earned * (1.0 + office_bonus / 100.0))

        # Phase 5: Synergy bonus
        synergy_bonus = sum(s["bonus"] for s in self.active_synergies)
        if synergy_bonus > 0:
            earned = int(earned * (1.0 + synergy_bonus / 100.0))

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
            # Phase 4: Track earnings
            self.month_earnings += earned
            self.year_earnings += earned
            self.month_mishaps += 1
            # Phase 5: Track mishap stats
            self.total_earnings += earned
            self.total_mishaps += 1
            self.consecutive_mishaps += 1
            self.consecutive_idles = 0

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
            self._phase5_post_turn()
            self._check_post_turn_events()
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
        # Phase 4: Track earnings
        self.month_earnings += earned
        self.year_earnings += earned
        # Phase 5: Track success stats
        self.total_earnings += earned
        self.consecutive_mishaps = 0
        self.consecutive_idles = 0
        self.completed_jobs.add(job["name"])

        a["exp"] += 15 if is_strong else 10
        # Memory expansion: 50% chance to skip fatigue gain
        has_fatigue_equip = self._has_equip("fatigue_reduce")
        has_office_fatigue = "負荷回復" in OFFICE_LEVELS[self.office_level].get("desc", "")
        if has_fatigue_equip and random.random() < 0.5:
            pass  # no fatigue gain this turn
        elif has_office_fatigue and random.random() < 0.3:
            pass  # office fatigue bonus
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

        # Overload warning
        if a["fatigue"] >= 6:
            self.turn_log.append("")
            self.turn_log.append("⚠ 負荷が高い…")
            self.naviko_msg = random.choice(NAVIKO_OVERLOAD)

        self.week += 1
        self.mishap_event = None
        # Phase 5: Check synergies (only on success path)
        new_synergies = self._check_synergies()
        for syn in new_synergies:
            self.turn_log.append("")
            self.turn_log.append(f"★ シナジー「{syn['name']}」発動！")
            self.turn_log.append(f"  {syn['desc']}")
        if new_synergies:
            self.naviko_msg = random.choice(NAVIKO_SYNERGY)
        self._phase5_post_turn()
        self._check_post_turn_events()
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
                if stat == strength_stat:
                    growth = 2  # 適性ステータス
                elif stat == "体力":
                    growth = 1  # 体力は固定+1
                else:
                    growth = 1  # その他ステータス
                agent["stats"][stat] = min(10, agent["stats"][stat] + growth)
            self.turn_log.append("")
            self.turn_log.append(f"★ Lv.{agent['level']}にアップ！")

    def _week_to_date(self, w):
        yr = (w - 1) // 48 + 1
        mo = ((w - 1) % 48) // 4 + 1
        wk = (w - 1) % 4 + 1
        return yr, mo, wk

    # ── Phase 5: Synergy / Title / Ending ──

    def _check_synergies(self):
        """Check if any new synergy combos have been unlocked."""
        new = []
        active_names = {s["name"] for s in self.active_synergies}
        for syn in SYNERGIES:
            if syn["name"] in active_names:
                continue
            if all(j in self.completed_jobs for j in syn["jobs"]):
                self.active_synergies.append(syn)
                new.append(syn)
        return new

    def _check_titles(self):
        """Check if any new titles have been earned."""
        new = []
        earned_ids = {t["id"] for t in self.earned_titles}
        for title in TITLES:
            if title["id"] in earned_ids:
                continue
            tid = title["id"]
            earned = False
            if tid == "loose_ceo" and self.consecutive_mishaps >= 10:
                earned = True
            elif tid == "emperor" and len(self.completed_jobs) >= len(ALL_JOBS):
                earned = True
            elif tid == "legend" and self.rep_rank >= 5:
                earned = True
            elif tid == "neet" and self.consecutive_idles >= 10:
                earned = True
            elif tid == "careful":
                if (self.agents and self.agents[0]["level"] >= 10
                        and self.total_mishaps == 0):
                    earned = True
            elif tid == "rich" and self.coins >= 100000:
                earned = True
            # "perfectionist" is checked at ending only
            if earned:
                self.earned_titles.append(title)
                new.append(title)
        return new

    def _phase5_post_turn(self):
        """Check titles after every turn and announce."""
        new_titles = self._check_titles()
        for t in new_titles:
            self.turn_log.append("")
            self.turn_log.append(f"★ 称号「{t['name']}」獲得！")
        if new_titles:
            self.naviko_msg = random.choice(NAVIKO_TITLE)

    def _determine_ending(self):
        """Determine which ending the player gets (priority order)."""
        has_lv5 = "AI組織運営" in self.completed_jobs
        # Empire: rep S + office max + Lv5 job done
        if self.rep_rank >= 5 and self.office_level >= 4 and has_lv5:
            return ENDINGS[0]  # empire
        # Rebellion: 50+ total mishaps
        if self.total_mishaps >= 50:
            return ENDINGS[1]  # rebellion
        # Stable: rep B+ (rank index >= 3)
        if self.rep_rank >= 3:
            return ENDINGS[2]  # stable
        # Small: rep D or lower (rank index <= 1)
        if self.rep_rank <= 1:
            return ENDINGS[3]  # small
        # Default (rep C or D range)
        return ENDINGS[4]  # default

    def _reset_game(self):
        """Reset all game state for a new playthrough."""
        self.scene = "title"
        self.week = 0
        self.coins = 0
        self.rep_rank = 0
        self.agents = []
        self.owned_equip = []
        self.office_level = 0
        self.available_jobs = []
        self.selected_job = None
        self.current_job = None
        self.turn_log = []
        self.turn_earned = 0
        self.mishap_event = None
        self.select_idx = 0
        self.naming_name = ""
        self.naviko_msg = ""
        self.job_scroll = 0
        self.equip_scroll = 0
        self.month_earnings = 0
        self.month_mishaps = 0
        self.year_earnings = 0
        self.pending_scenes = []
        self.prev_rep_rank = 0
        self.rankup_from = 0
        self.report_data = {}
        self.tax_year_income = 0
        self.total_mishaps = 0
        self.consecutive_mishaps = 0
        self.consecutive_idles = 0
        self.completed_jobs = set()
        self.earned_titles = []
        self.active_synergies = []
        self.total_earnings = 0
        self._scene_comment = ""
        self.ending_data = None
        self.work_timer = 0
        self._setup_scene()

    # Phase 5: Ending scene

    def update_ending(self):
        if self.buttons["restart"].clicked():
            self._reset_game()

    def draw_ending(self):
        pyxel.cls(C_BLACK)
        end = self.ending_data
        if not end:
            return

        # Sparkle animation for empire ending
        frame = pyxel.frame_count
        if end["id"] == "empire":
            for i in range(12):
                sx = (i * 23 + frame * 2) % WIDTH
                sy = (i * 13 + frame) % 30
                pyxel.pset(sx, sy, C_YELLOW if (frame + i) % 2 else C_WHITE)

        # Title
        title_col = C_YELLOW if end["id"] == "empire" else C_WHITE
        text_centered(14, f"~ {end['name']} ~", title_col, self.font)
        pyxel.line(0, 32, WIDTH, 32, C_DGRAY)

        # Description
        y = 42
        for line in end["desc"].split("\n"):
            text_centered(y, line, C_WHITE, self.font_s)
            y += 16

        # Stats summary
        y += 4
        pyxel.line(20, y, 220, y, C_DGRAY)
        y += 8
        stats = [
            ("総収益", f"{self.total_earnings}G", C_GREEN),
            ("やらかし", f"{self.total_mishaps}回",
             C_PINK if self.total_mishaps > 0 else C_WHITE),
            ("評判", REP_RANKS[self.rep_rank], C_YELLOW),
        ]
        if self.agents:
            stats.append(("AI Lv", str(self.agents[0]["level"]), C_SKYBLUE))
        stats.append(("事務所", OFFICE_LEVELS[self.office_level]["name"], C_WHITE))
        stats.append((
            "副業制覇",
            f"{len(self.completed_jobs)}/{len(ALL_JOBS)}",
            C_GREEN if len(self.completed_jobs) >= len(ALL_JOBS) else C_WHITE,
        ))

        for label, value, col in stats:
            pyxel.text(36, y, label, C_GRAY, self.font_s)
            pyxel.text(148, y, value, col, self.font_s)
            y += 14

        # Titles earned
        if self.earned_titles:
            y += 4
            pyxel.text(36, y, "獲得称号:", C_YELLOW, self.font_s)
            y += 14
            for t in self.earned_titles[:3]:
                pyxel.text(44, y, f"★ {t['name']}", C_SKYBLUE, self.font_s)
                y += 14
            if len(self.earned_titles) > 3:
                pyxel.text(44, y, f"  他{len(self.earned_titles) - 3}個", C_GRAY, self.font_s)

        # Naviko comment area
        nav_y = 236
        pyxel.rect(0, nav_y, WIDTH, 38, C_NAVY)
        pyxel.rectb(0, nav_y, WIDTH, 38, C_DGRAY)
        pyxel.blt(1, nav_y + 3, 0, 192, 0, 32, 32, SPRITE_COLKEY)
        naviko = end.get("naviko", "")
        lines = naviko.split("\n")
        for i, line in enumerate(lines[:3]):
            pyxel.text(32, nav_y + 4 + i * 12, line, C_WHITE, self.font_s)

        # Restart button
        self.buttons["restart"].draw(self.font, C_DGREEN, C_WHITE, C_GREEN)

    # ── Draw dispatch ──

    def draw(self):
        pyxel.cls(C_NAVY)
        fn = getattr(self, f"draw_{self.scene}", None)
        if fn:
            fn()

    def draw_title(self):
        pyxel.cls(C_BLACK)
        text_centered(160, "自動化帝国", C_YELLOW, self.font)
        text_centered(190, "AI副業経営シミュレーション", C_WHITE, self.font_s)
        if pyxel.frame_count % 60 < 40:
            text_centered(340, "タップしてスタート", C_GRAY, self.font_s)
        text_centered(460, "v0.5 - Phase 5", C_DGRAY, self.font_s)

    def draw_select(self):
        pyxel.cls(C_BLACK)
        text_centered(18, "パートナーを選べ", C_YELLOW, self.font)
        text_centered(38, "タップして選択", C_GRAY, self.font_s)

        for i, st in enumerate(STARTERS):
            b = self.buttons[f"c{i}"]
            pyxel.rect(b.x, b.y, b.w, b.h, C_NAVY)
            pyxel.rectb(b.x, b.y, b.w, b.h, st["color"])

            # Avatar
            ax, ay = b.x + 18, b.y + 35
            self._draw_avatar_small(st["id"], ax, ay, st["color"])

            # Text
            tx = b.x + 60
            pyxel.text(tx, b.y + 10, st["name"], C_WHITE, self.font)
            pyxel.text(tx, b.y + 30, st["type_label"], st["color"], self.font_s)
            for j, line in enumerate(st["desc"].split("\n")):
                pyxel.text(tx, b.y + 52 + j * 16, line, C_GRAY, self.font_s)

    def draw_naming(self):
        pyxel.cls(C_BLACK)
        st = STARTERS[self.select_idx]

        text_centered(20, "名前をつけよう", C_YELLOW, self.font)
        self._draw_avatar_large(st["id"], 135, 120, st["color"])
        text_centered(165, st["type_label"], st["color"], self.font_s)

        # Name display panel
        draw_panel(45, 240, 180, 40, C_NAVY, C_GRAY)
        text_centered(250, self.naming_name, C_WHITE, self.font)

        # Buttons
        self.buttons["rand"].draw(self.font_s, C_DGRAY, C_WHITE, C_GRAY)
        self.buttons["ok"].draw(self.font, C_DGREEN, C_WHITE, C_GREEN)

    def draw_office(self):
        # Status bar
        pyxel.rect(0, 0, WIDTH, 24, C_BLACK)
        pyxel.text(6, 7, f"{self.coins}G", C_YELLOW, self.font_s)
        rank = REP_RANKS[self.rep_rank]
        pyxel.text(100, 7, f"評判:{rank}", C_WHITE, self.font_s)
        if self.week > 0:
            yr, mo, _ = self._week_to_date(self.week)
            pyxel.text(200, 7, f"{yr}年{mo}月", C_GRAY, self.font_s)

        # Office area (expanded for 9:16)
        pyxel.rect(0, 24, WIDTH, 230, C_NAVY)

        # Phase 4: Office visuals based on level
        if self.office_level >= 4:
            pyxel.rect(0, 24, WIDTH, 4, C_YELLOW)
            pyxel.rect(0, 236, WIDTH, 3, C_YELLOW)
        elif self.office_level >= 3:
            pyxel.rect(0, 236, WIDTH, 3, C_GREEN)
        elif self.office_level >= 2:
            pyxel.rect(0, 236, WIDTH, 3, C_SKYBLUE)

        # Floor line
        pyxel.line(0, 240, WIDTH, 240, C_DGRAY)
        # Desk
        desk_col = C_BROWN if self.office_level < 3 else C_ORANGE
        pyxel.rect(75, 210, 120, 18, desk_col)
        # Monitor
        pyxel.rect(110, 186, 50, 24, C_DGRAY)
        monitor_col = C_SKYBLUE if self.office_level < 4 else C_GREEN
        pyxel.rect(114, 190, 42, 16, monitor_col)

        # Phase 4: Extra furniture for higher office levels
        if self.office_level >= 2:
            pyxel.rect(12, 180, 28, 48, C_BROWN)
            pyxel.line(12, 192, 39, 192, C_DGRAY)
            pyxel.line(12, 204, 39, 204, C_DGRAY)
            pyxel.line(12, 216, 39, 216, C_DGRAY)
        if self.office_level >= 3:
            pyxel.rect(230, 180, 28, 48, C_DGRAY)
            pyxel.rect(234, 188, 20, 5, C_GREEN)
            pyxel.rect(234, 200, 20, 5, C_SKYBLUE)
            pyxel.rect(234, 212, 20, 5, C_GREEN)

        # Agent at desk
        if self.agents:
            a = self.agents[0]
            bob = -2 if (pyxel.frame_count // 20) % 2 else 0
            self._draw_avatar_small(a["id"], 123, 150 + bob, a["color"])

        # Current job indicator
        if self.current_job:
            pyxel.text(10, 248, f"受注中: {self.current_job['name']}", C_GREEN, self.font_s)
        else:
            pyxel.text(10, 248, "案件未選択", C_DGRAY, self.font_s)

        # Phase 4: Office name
        office_name = OFFICE_LEVELS[self.office_level]["name"]
        pyxel.text(165, 248, office_name, C_GRAY, self.font_s)

        # Naviko message area
        pyxel.rect(0, 268, WIDTH, 60, C_BLACK)
        pyxel.rectb(0, 268, WIDTH, 60, C_DGRAY)
        self._draw_naviko_icon(2, 272)
        for i, line in enumerate(self.naviko_msg.split("\n")):
            pyxel.text(44, 276 + i * 16, line, C_WHITE, self.font_s)

        # Bottom buttons
        for key in ("jobs", "ai", "equip"):
            self.buttons[key].draw(self.font_s, C_DGRAY, C_WHITE, C_GRAY)
        self.buttons["next"].draw(self.font_s, C_DGREEN, C_WHITE, C_GREEN)

    def draw_working(self):
        """Working/processing animation screen."""
        pyxel.cls(C_BLACK)
        frame = self.work_timer

        # Determine what's happening
        is_defrag = getattr(self, '_is_defragging', False)
        if is_defrag:
            title = "デフラグ中..."
            sub = "負荷をリセットしています"
        elif self.current_job:
            title = "作業中..."
            sub = f"「{self.current_job['name']}」を実行中"
        else:
            title = "時間経過..."
            sub = "1週間が過ぎていく..."

        # Title
        text_centered(100, title, C_YELLOW, self.font)
        text_centered(130, sub, C_GRAY, self.font_s)

        # AI avatar bouncing
        if self.agents:
            a = self.agents[0]
            bounce = abs((frame % 30) - 15) - 8
            self._draw_avatar_large(a["id"], 135, 210 + bounce, a["color"])

        # Progress bar
        bar_x, bar_y, bar_w, bar_h = 40, 290, 190, 16
        pyxel.rect(bar_x, bar_y, bar_w, bar_h, C_DGRAY)
        progress = min(frame / 90.0, 1.0)
        fill_w = int(bar_w * progress)
        bar_col = C_GREEN if not is_defrag else C_SKYBLUE
        if fill_w > 0:
            pyxel.rect(bar_x, bar_y, fill_w, bar_h, bar_col)
        pyxel.rectb(bar_x, bar_y, bar_w, bar_h, C_GRAY)

        # Percentage
        pct = int(progress * 100)
        text_centered(312, f"{pct}%", C_WHITE, self.font_s)

        # Animated dots
        dots = "." * ((frame // 10) % 4)
        text_centered(340, dots, C_GRAY, self.font_s)

        # Naviko comment
        naviko_msgs = [
            "がんばれがんばれ…", "処理中…もうちょい。",
            "ふむふむ…", "順調だよ。",
        ]
        msg_idx = (frame // 30) % len(naviko_msgs)
        pyxel.rect(0, 380, WIDTH, 50, C_NAVY)
        pyxel.rectb(0, 380, WIDTH, 50, C_DGRAY)
        pyxel.blt(2, 389, 0, 192, 0, 32, 32, SPRITE_COLKEY)
        pyxel.text(34, 396, naviko_msgs[msg_idx], C_WHITE, self.font_s)

    def draw_result(self):
        pyxel.cls(C_BLACK)

        if self.mishap_event:
            text_centered(16, "!! やらかし発生 !!", C_RED, self.font)
        else:
            text_centered(16, "今週の結果", C_YELLOW, self.font)

        y = 60
        for line in self.turn_log:
            if line == "":
                y += 8
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
            y += 20

        # Show mishap detail
        if self.mishap_event:
            y += 6
            pyxel.rect(20, y, 230, 68, C_NAVY)
            pyxel.rectb(20, y, 230, 68, C_RED)
            for i, line in enumerate(self.mishap_event["text"].split("\n")):
                pyxel.text(28, y + 10 + i * 16, line, C_PINK, self.font_s)
            y += 74

        self.buttons["cont"].draw(self.font, C_DGRAY, C_WHITE, C_GRAY)

    def draw_mishap(self):
        pyxel.cls(C_BLACK)

        # Header
        text_centered(10, "どうする？", C_RED, self.font)
        pyxel.line(0, 28, WIDTH, 28, C_DGRAY)

        # Mishap text (up to 3 lines)
        if self.mishap_event:
            y = 36
            for line in self.mishap_event["text"].split("\n"):
                text_centered(y, line, C_PINK, self.font_s)
                y += 16

        # Naviko comment area
        pyxel.rect(0, 96, WIDTH, 56, C_NAVY)
        pyxel.rectb(0, 96, WIDTH, 56, C_DGRAY)
        pyxel.blt(2, 104, 0, 192, 0, 32, 32, SPRITE_COLKEY)
        msg_lines = self.naviko_msg.split("\n") if self.naviko_msg else ["..."]
        pyxel.text(34, 104, msg_lines[0], C_WHITE, self.font_s)
        if len(msg_lines) > 1:
            pyxel.text(34, 120, msg_lines[1], C_WHITE, self.font_s)
        if len(msg_lines) > 2:
            pyxel.text(34, 136, msg_lines[2], C_WHITE, self.font_s)

        # Choice buttons
        if self.mishap_event:
            choices = self.mishap_event.get("choices", [])
            for i, choice in enumerate(choices):
                key = f"ch{i}"
                if key in self.buttons:
                    btn = self.buttons[key]
                    pyxel.rect(btn.x, btn.y, btn.w, btn.h, C_NAVY)
                    pyxel.rectb(btn.x, btn.y, btn.w, btn.h, C_GRAY)
                    lines = choice["text"].split("\n")
                    if len(lines) == 1:
                        pyxel.text(btn.x + 10, btn.y + (btn.h - 12) // 2, lines[0], C_WHITE, self.font_s)
                    else:
                        pyxel.text(btn.x + 10, btn.y + 10, lines[0], C_WHITE, self.font_s)
                        pyxel.text(btn.x + 10, btn.y + 26, lines[1], C_WHITE, self.font_s)

    # Phase 4: Monthly report screen

    def draw_monthly_report(self):
        pyxel.cls(C_BLACK)

        d = self.report_data
        mo = d.get("month", 1)
        yr = d.get("year", 1)

        text_centered(16, f"{yr}年目 {mo}月のレポート", C_YELLOW, self.font)
        pyxel.line(0, 36, WIDTH, 36, C_DGRAY)

        # Stats
        y = 70
        items = [
            ("収益", f"{d.get('earnings', 0)}G", C_GREEN),
            ("やらかし", f"{d.get('mishaps', 0)}回", C_PINK if d.get('mishaps', 0) > 0 else C_WHITE),
            ("評判", d.get("rank", "E"), C_YELLOW),
            ("AI Lv", str(d.get("level", 1)), C_SKYBLUE),
            ("所持金", f"{self.coins}G", C_GREEN),
        ]

        for label, value, col in items:
            pyxel.text(50, y, label, C_GRAY, self.font_s)
            pyxel.text(160, y, value, col, self.font_s)
            y += 30

        # Naviko comment
        pyxel.rect(0, 300, WIDTH, 60, C_NAVY)
        pyxel.rectb(0, 300, WIDTH, 60, C_DGRAY)
        pyxel.blt(2, 310, 0, 192, 0, 32, 32, SPRITE_COLKEY)

        comment = self._scene_comment
        lines = comment.split("\n")
        pyxel.text(34, 308, lines[0], C_WHITE, self.font_s)
        if len(lines) > 1:
            pyxel.text(34, 324, lines[1], C_WHITE, self.font_s)
        if len(lines) > 2:
            pyxel.text(34, 340, lines[2], C_WHITE, self.font_s)

        self.buttons["cont"].draw(self.font, C_DGRAY, C_WHITE, C_GRAY)

    # Phase 4: Rank up screen

    def draw_rankup(self):
        pyxel.cls(C_BLACK)

        # Sparkle animation
        frame = pyxel.frame_count
        for i in range(8):
            sx = 40 + (i * 30 + frame * 2) % 200
            sy = 20 + (i * 17 + frame) % 60
            col = C_YELLOW if (frame + i) % 3 else C_WHITE
            pyxel.pset(sx, sy, col)

        text_centered(90, "★ ランクアップ！ ★", C_YELLOW, self.font)

        old_rank = REP_RANKS[self.rankup_from]
        new_rank = REP_RANKS[self.rep_rank]
        text_centered(130, f"{old_rank} → {new_rank}", C_WHITE, self.font)

        # Rank name
        rank_names = {
            "E": "無名", "D": "そこそこ", "C": "中堅",
            "B": "有名", "A": "トップ", "S": "伝説",
        }
        rank_desc = rank_names.get(new_rank, "")
        text_centered(160, f"「{rank_desc}」", C_SKYBLUE, self.font_s)

        # Naviko comment
        pyxel.rect(0, 190, WIDTH, 50, C_NAVY)
        pyxel.rectb(0, 190, WIDTH, 50, C_YELLOW)
        pyxel.blt(1, 199, 0, 192, 0, 32, 32, SPRITE_COLKEY)
        comment = self._scene_comment
        lines = comment.split("\n")
        pyxel.text(32, 198, lines[0], C_WHITE, self.font_s)
        if len(lines) > 1:
            pyxel.text(32, 212, lines[1], C_WHITE, self.font_s)

        self.buttons["cont"].draw(self.font, C_DGRAY, C_WHITE, C_GRAY)

    # Phase 4: Tax event screen

    def draw_tax_event(self):
        pyxel.cls(C_BLACK)

        text_centered(10, "確定申告の季節！", C_YELLOW, self.font)
        pyxel.line(0, 28, WIDTH, 28, C_DGRAY)

        # Income summary
        text_centered(44, f"1年間の収益: {self.tax_year_income}G", C_WHITE, self.font_s)

        # Naviko comment
        pyxel.rect(0, 66, WIDTH, 44, C_NAVY)
        pyxel.rectb(0, 66, WIDTH, 44, C_DGRAY)
        pyxel.blt(1, 73, 0, 192, 0, 32, 32, SPRITE_COLKEY)
        comment = self._scene_comment
        lines = comment.split("\n")
        pyxel.text(32, 72, lines[0], C_WHITE, self.font_s)
        if len(lines) > 1:
            pyxel.text(32, 86, lines[1], C_WHITE, self.font_s)
        if len(lines) > 2:
            pyxel.text(32, 100, lines[2], C_WHITE, self.font_s)

        # Tax choice buttons
        tax_labels = [
            "自分で申告する",
            "AIに任せる",
            "税理士に依頼する",
            "放置する",
        ]
        for i in range(4):
            key = f"tax{i}"
            if key in self.buttons:
                btn = self.buttons[key]
                bg = C_NAVY
                border = C_GRAY
                if i == 0:
                    border = C_GREEN
                elif i == 1:
                    border = C_ORANGE
                elif i == 3:
                    border = C_RED
                pyxel.rect(btn.x, btn.y, btn.w, btn.h, bg)
                pyxel.rectb(btn.x, btn.y, btn.w, btn.h, border)
                pyxel.text(btn.x + 8, btn.y + (btn.h - 12) // 2, tax_labels[i], C_WHITE, self.font_s)

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

        # Clean up ghost scroll buttons from previous frame
        self.buttons.pop("scroll_up", None)
        self.buttons.pop("scroll_down", None)

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

        # Scroll buttons
        if self.job_scroll > 0:
            self.buttons["scroll_up"] = Button(120, 34, 100, 20, "▲ 上へ")
            self.buttons["scroll_up"].draw(self.font_s, C_DGRAY, C_GRAY, C_GRAY)
        if self.job_scroll + 4 < len(self.available_jobs):
            self.buttons["scroll_down"] = Button(120, 260, 100, 20, "▼ 下へ")
            self.buttons["scroll_down"].draw(self.font_s, C_DGRAY, C_GRAY, C_GRAY)

        self.buttons["back"].draw(self.font_s, C_DGRAY, C_WHITE, C_GRAY)

    def draw_equip_shop(self):
        pyxel.cls(C_BLACK)
        text_centered(10, "設備ショップ", C_YELLOW, self.font)
        pyxel.text(8, 28, f"所持金: {self.coins}G", C_GREEN, self.font_s)

        has_office_btn = self.office_level < len(OFFICE_LEVELS) - 1

        # Phase 4: Office upgrade at top
        if has_office_btn:
            next_lv = OFFICE_LEVELS[self.office_level + 1]
            cur_name = OFFICE_LEVELS[self.office_level]["name"]
            can_buy = self.coins >= next_lv["cost"]

            btn = self.buttons.get("office_up")
            if btn:
                bg = C_DGREEN if can_buy else C_DGRAY
                border = C_YELLOW if can_buy else C_GRAY
                draw_panel(btn.x, btn.y, btn.w, btn.h, bg, border)
                pyxel.text(btn.x + 8, btn.y + 6, f"{cur_name} → {next_lv['name']}", C_WHITE, self.font_s)
                pyxel.text(btn.x + 8, btn.y + 22, next_lv["desc"], C_GRAY, self.font_s)
                cost_col = C_YELLOW if can_buy else C_RED
                pyxel.text(btn.x + 140, btn.y + 6, f"{next_lv['cost']}G", cost_col, self.font_s)
                pyxel.text(btn.x + 8, btn.y + 36, "事務所拡張", C_YELLOW, self.font_s)

        # Equipment list
        eq_y_start = 110 if has_office_btn else 44
        visible = self._visible_equips()
        if not visible and not has_office_btn:
            text_centered(140, "設備がありません", C_DGRAY, self.font_s)
        else:
            for i, eq in enumerate(visible):
                y = eq_y_start + i * 64
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

                draw_panel(16, y, 208, 56, bg_col, border_col)
                pyxel.text(24, y + 8, eq["name"], C_WHITE, self.font_s)
                pyxel.text(24, y + 28, eq["desc"], C_GRAY, self.font_s)

                if owned:
                    pyxel.text(160, y + 8, "購入済", C_GRAY, self.font_s)
                else:
                    cost_col = C_GREEN if can_buy else C_RED
                    pyxel.text(150, y + 8, f"{eq['cost']}G", cost_col, self.font_s)

        # Scroll buttons
        if self.equip_scroll > 0:
            self.buttons["scroll_up"] = Button(120, eq_y_start - 14, 100, 20, "▲ 上へ")
            self.buttons["scroll_up"].draw(self.font_s, C_DGRAY, C_GRAY, C_GRAY)
        max_visible = 3 if has_office_btn else 4
        scroll_down_y = eq_y_start + max_visible * 64 + 4
        if self.equip_scroll + max_visible < len(EQUIPMENTS):
            self.buttons["scroll_down"] = Button(120, scroll_down_y, 100, 20, "▼ 下へ")
            self.buttons["scroll_down"].draw(self.font_s, C_DGRAY, C_GRAY, C_GRAY)

        self.buttons["back"].draw(self.font_s, C_DGRAY, C_WHITE, C_GRAY)

    # ── Avatar drawing ──

    def _draw_avatar_small(self, agent_id, cx, cy, col):
        """Draw a 64x64 sprite centered at (cx, cy)."""
        uv = SPRITE_UV.get(agent_id)
        if uv:
            pyxel.blt(cx - SPRITE_SZ // 2, cy - SPRITE_SZ // 2, 0,
                       uv[0], uv[1], SPRITE_SZ, SPRITE_SZ, SPRITE_COLKEY)
        else:
            pyxel.circ(cx, cy, 20, col)

    def _draw_avatar_large(self, agent_id, cx, cy, col):
        """Draw a 64x64 sprite centered at (cx, cy)."""
        uv = SPRITE_UV.get(agent_id)
        if uv:
            pyxel.blt(cx - SPRITE_SZ // 2, cy - SPRITE_SZ // 2, 0,
                       uv[0], uv[1], SPRITE_SZ, SPRITE_SZ, SPRITE_COLKEY)
        else:
            pyxel.circ(cx, cy, 28, col)

    def _draw_naviko_icon(self, x, y, size=40):
        """Draw nabiko face icon for comment panels (cropped from 64x64)."""
        nu, nv = SPRITE_UV["nabiko"]
        offset = (SPRITE_SZ - size) // 2
        pyxel.blt(x, y, 0, nu + offset, nv, size, size, SPRITE_COLKEY)
