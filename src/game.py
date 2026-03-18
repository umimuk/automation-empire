"""メインゲームクラス - 自動化帝国"""

import pyxel
from src.constants import *
from src.ai_agent import AIAgent
from src.jobs import JobManager
from src.incidents import IncidentEngine
from src.text_util import (
    draw_text, draw_text_center, draw_text_shadow,
    draw_text_center_shadow, format_number,
)


class Game:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="Automation Empire", fps=FPS)

        # ゲーム状態
        self.scene = SCENE_TITLE
        self.prev_scene = SCENE_TITLE
        self.coins = 0
        self.total_coins = 0
        self.click_power = BASE_CLICK_INCOME
        self.ai_agent = None
        self.frame_count = 0

        # マネージャー
        self.job_mgr = JobManager()
        self.incident_engine = IncidentEngine()

        # UI状態
        self.selected_ai_index = 0
        self.tutorial_step = 0
        self.click_effects = []
        self.coin_anim = 0

        # 御三家描画位置
        self.ai_positions = [
            (40, 120), (108, 120), (176, 120),
        ]

        # 名前入力
        self.name_input = ""
        self.name_cursor_blink = 0

        # ナビ子
        self.naviko_msg = ""
        self.naviko_timer = 0
        self.naviko_visible = False
        self.naviko_flicker = 0

        # メイン画面
        self.auto_income_timer = 0
        self.tutorial_done = False
        self.route_prompted = False  # ルート選択を促したか
        self.show_shop = False

        # ルート選択
        self.route_cursor = 0

        # やらかしイベント
        self.current_event = None
        self.event_choice_cursor = 0
        self.event_result = None
        self.event_result_timer = 0

        # ショップ
        self.shop_cursor = 0
        self.shop_items = []

        # 通知メッセージ
        self.notification = ""
        self.notification_timer = 0

        pyxel.run(self.update, self.draw)

    # ========== UPDATE ==========

    def update(self):
        self.frame_count += 1

        # クリックエフェクト更新
        self.click_effects = [
            {**e, "timer": e["timer"] - 1, "y": e["y"] - 0.5}
            for e in self.click_effects if e["timer"] > 0
        ]

        # ナビ子ホログラム演出
        if self.naviko_visible:
            self.naviko_flicker = (self.naviko_flicker + 1) % 60
            if self.naviko_timer > 0:
                self.naviko_timer -= 1
                if self.naviko_timer == 0:
                    self.naviko_visible = False

        # 通知タイマー
        if self.notification_timer > 0:
            self.notification_timer -= 1
            if self.notification_timer == 0:
                self.notification = ""

        if self.scene == SCENE_TITLE:
            self._update_title()
        elif self.scene == SCENE_SELECT_AI:
            self._update_select_ai()
        elif self.scene == SCENE_NAME_INPUT:
            self._update_name_input()
        elif self.scene == SCENE_TUTORIAL:
            self._update_tutorial()
        elif self.scene == SCENE_MAIN:
            self._update_main()
        elif self.scene == SCENE_ROUTE_SELECT:
            self._update_route_select()
        elif self.scene == SCENE_EVENT:
            self._update_event()
        elif self.scene == SCENE_SHOP:
            self._update_shop()

    def _update_title(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_SELECT_AI
            self._show_naviko(NAVIKO_LINES["select_intro"], 0)

    def _update_select_ai(self):
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.selected_ai_index = (self.selected_ai_index - 1) % 3
            self._show_ai_description()
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.selected_ai_index = (self.selected_ai_index + 1) % 3
            self._show_ai_description()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            for i, (ax, ay) in enumerate(self.ai_positions):
                if ax - 20 <= mx <= ax + 20 and ay - 20 <= my <= ay + 20:
                    self.selected_ai_index = i
                    self._show_ai_description()
                    break

        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self.ai_agent = AIAgent(self.selected_ai_index)
            self.name_input = self.ai_agent.name
            self.scene = SCENE_NAME_INPUT

    def _show_ai_description(self):
        descs = ["poem_desc", "bugmaru_desc", "hattari_desc"]
        self._show_naviko(NAVIKO_LINES[descs[self.selected_ai_index]], 0)

    def _update_name_input(self):
        self.name_cursor_blink = (self.name_cursor_blink + 1) % 40

        for key in range(pyxel.KEY_A, pyxel.KEY_Z + 1):
            if pyxel.btnp(key):
                if len(self.name_input) < 8:
                    ch = chr(key - pyxel.KEY_A + ord('A'))
                    if not pyxel.btn(pyxel.KEY_SHIFT):
                        ch = ch.lower()
                    self.name_input += ch
        for key in range(pyxel.KEY_0, pyxel.KEY_9 + 1):
            if pyxel.btnp(key):
                if len(self.name_input) < 8:
                    self.name_input += chr(key - pyxel.KEY_0 + ord('0'))

        if pyxel.btnp(pyxel.KEY_BACKSPACE) and self.name_input:
            self.name_input = self.name_input[:-1]

        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.name_input.strip():
                self.ai_agent.rename(self.name_input)
            msg = NAVIKO_LINES["selected"].format(name=self.ai_agent.name)
            self._show_naviko(msg, 90)
            self.scene = SCENE_TUTORIAL
            self.tutorial_step = 0

    def _update_tutorial(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_RETURN):
            self.tutorial_step += 1
            if self.tutorial_step >= len(TUTORIAL_MESSAGES):
                self.tutorial_done = True
                self.scene = SCENE_MAIN
                # 最初の副業を無料でアンロック
                self.job_mgr.owned_jobs = [0]
                self.job_mgr.active_jobs = [0]
                msg = NAVIKO_LINES["tutorial_click"].format(
                    name=self.ai_agent.name
                )
                self._show_naviko(msg, 150)

    def _update_main(self):
        # クリック処理
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y

            # ショップボタン判定
            if 200 <= mx <= 252 and 26 <= my <= 42:
                self._open_shop()
                return

            # クリックエリア判定
            if 30 <= my <= 200:
                income = self._calc_click_income()
                self.coins += income
                self.total_coins += income
                self.coin_anim = 10

                if self.ai_agent:
                    leveled = self.ai_agent.add_exp(AI_EXP_PER_CLICK)
                    if leveled:
                        self._on_level_up()

                self.click_effects.append({
                    "x": mx, "y": my,
                    "text": f"+{format_number(income)}",
                    "timer": 20,
                })

        # Sキーでショップ
        if pyxel.btnp(pyxel.KEY_S):
            self._open_shop()
            return

        # 自動収入（1秒ごと）
        self.auto_income_timer += 1
        if self.auto_income_timer >= FPS:
            self.auto_income_timer = 0
            if self.ai_agent and self.job_mgr.active_jobs:
                auto = self._calc_auto_income()
                if auto > 0:
                    self.coins += auto
                    self.total_coins += auto

            # やらかし判定（1秒ごと）
            if self.ai_agent:
                event = self.incident_engine.check_incident(self.ai_agent)
                if event:
                    self._trigger_event(event)
                    return

        if self.coin_anim > 0:
            self.coin_anim -= 1

    def _on_level_up(self):
        """レベルアップ時の処理"""
        lv = self.ai_agent.level
        name = self.ai_agent.name
        msg = NAVIKO_LINES["level_up"].format(name=name, level=lv)
        self._show_naviko(msg, 90)
        self._notify(f"{name} Lv{lv}!")

        # ルート選択チェック
        if (self.job_mgr.needs_route_selection(lv, self.ai_agent.route)
                and not self.route_prompted):
            self.route_prompted = True
            self._show_naviko(
                NAVIKO_LINES["route_select"].format(name=name), 0
            )
            self.scene = SCENE_ROUTE_SELECT
            self.route_cursor = 0
            return

        # 新しい副業レベルのアンロック通知
        for job_lv, required in UNLOCK_REQUIREMENTS.items():
            if lv == required and job_lv > 1:
                if job_lv == 4:
                    self._notify("Lv4 gigs unlocked! Check shop.")
                    self._show_naviko(NAVIKO_LINES["lv4_merge"], 120)
                elif job_lv == 5:
                    self._notify("Lv5: AI Empire unlocked!")
                    self._show_naviko(NAVIKO_LINES["lv5_empire"], 120)
                else:
                    self._notify(f"Lv{job_lv} gigs unlocked!")

    def _update_route_select(self):
        """ルート選択画面"""
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.route_cursor = (self.route_cursor - 1) % 3
            descs = ["route_creator", "route_tech", "route_business"]
            self._show_naviko(NAVIKO_LINES[descs[self.route_cursor]], 0)
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.route_cursor = (self.route_cursor + 1) % 3
            descs = ["route_creator", "route_tech", "route_business"]
            self._show_naviko(NAVIKO_LINES[descs[self.route_cursor]], 0)

        # マウスクリックで選択
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            positions = [(40, 100), (128, 100), (216, 100)]
            for i, (rx, ry) in enumerate(positions):
                if rx - 30 <= mx <= rx + 30 and ry - 20 <= my <= ry + 20:
                    self.route_cursor = i
                    descs = ["route_creator", "route_tech", "route_business"]
                    self._show_naviko(NAVIKO_LINES[descs[i]], 0)
                    break

        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self.ai_agent.set_route(self.route_cursor)
            route_name = ROUTE_NAMES[self.route_cursor]

            # 適性チェック
            if self.route_cursor == self.ai_agent.aptitude_route:
                msg = NAVIKO_LINES["route_aptitude"].format(
                    route=route_name, name=self.ai_agent.name
                )
            elif abs(self.route_cursor - self.ai_agent.aptitude_route) == 2:
                msg = NAVIKO_LINES["route_mismatch"].format(
                    route=route_name, name=self.ai_agent.name
                )
            else:
                msg = NAVIKO_LINES["route_chosen"].format(
                    route=route_name, name=self.ai_agent.name
                )
            self._show_naviko(msg, 120)
            self._notify(f"Route: {route_name}!")
            self.scene = SCENE_MAIN

    def _update_event(self):
        """やらかしイベント画面"""
        if self.event_result:
            # 結果表示中
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_RETURN):
                self.scene = SCENE_MAIN
                self.current_event = None
                self.event_result = None
            return

        # 選択肢カーソル
        choices = self.current_event["choices"]
        if pyxel.btnp(pyxel.KEY_UP):
            self.event_choice_cursor = (self.event_choice_cursor - 1) % len(choices)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.event_choice_cursor = (self.event_choice_cursor + 1) % len(choices)

        # マウスクリックで選択
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            for i in range(len(choices)):
                cy = 160 + i * 20
                if 30 <= mx <= 226 and cy - 2 <= my <= cy + 12:
                    self.event_choice_cursor = i
                    self._apply_event_choice(i)
                    return

        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self._apply_event_choice(self.event_choice_cursor)

    def _apply_event_choice(self, choice_index):
        """イベント選択肢を適用"""
        result = self.incident_engine.apply_choice(
            self.current_event, choice_index
        )
        self.event_result = result

        # コイン効果
        self.coins += result["coin_effect"]
        if self.coins < 0:
            self.coins = 0

        # AIのやらかしカウント
        if self.ai_agent:
            self.ai_agent.incident_count += 1

        # ナビ子のコメント
        result_type = result["result"]
        if result_type == "good":
            naviko = NAVIKO_LINES["incident_good"]
        elif result_type == "bad":
            naviko = NAVIKO_LINES["incident_bad"]
        else:
            naviko = NAVIKO_LINES["incident_neutral"]
        self._show_naviko(naviko, 90)

    def _update_shop(self):
        """ショップ画面"""
        if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.KEY_S):
            self.scene = SCENE_MAIN
            return

        if not self.shop_items:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_RETURN):
                self.scene = SCENE_MAIN
            return

        if pyxel.btnp(pyxel.KEY_UP):
            self.shop_cursor = (self.shop_cursor - 1) % len(self.shop_items)
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.shop_cursor = (self.shop_cursor + 1) % len(self.shop_items)

        # マウスクリックで選択
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            for i in range(len(self.shop_items)):
                iy = 50 + i * 22
                if 10 <= mx <= 246 and iy - 2 <= my <= iy + 18:
                    self.shop_cursor = i
                    break

        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            if self.shop_cursor < len(self.shop_items):
                job = self.shop_items[self.shop_cursor]
                result = self.job_mgr.buy_job(job["id"], self.coins)
                if result:
                    self.coins = result[0]
                    bought_job = result[1]
                    msg = NAVIKO_LINES["job_unlock"].format(
                        job_name=bought_job["name"],
                        desc=bought_job["desc"],
                    )
                    self._show_naviko(msg, 120)
                    self._notify(f"Bought: {bought_job['name']}!")
                    # ショップ商品を更新
                    self._refresh_shop()
                else:
                    self._notify("Not enough coins!")

    def _open_shop(self):
        """ショップを開く"""
        self.prev_scene = self.scene
        self.scene = SCENE_SHOP
        self.shop_cursor = 0
        self._refresh_shop()

    def _refresh_shop(self):
        """ショップの商品リストを更新"""
        if self.ai_agent:
            self.shop_items = self.job_mgr.get_available_jobs(
                self.ai_agent.level, self.ai_agent.route
            )
        else:
            self.shop_items = []

    def _trigger_event(self, event):
        """やらかしイベントを発生させる"""
        self.current_event = event
        self.event_choice_cursor = 0
        self.event_result = None
        self.prev_scene = self.scene
        self.scene = SCENE_EVENT
        self._show_naviko(NAVIKO_LINES["incident_intro"], 60)

    def _calc_click_income(self):
        """クリック収入を計算"""
        base = self.click_power + self.job_mgr.calc_click_bonus()
        return base

    def _calc_auto_income(self):
        """自動収入を計算（1秒あたり）"""
        if not self.ai_agent:
            return 0
        return int(self.ai_agent.auto_income * self.job_mgr.calc_auto_bonus())

    def _show_naviko(self, msg, duration=0):
        self.naviko_msg = msg
        self.naviko_timer = duration
        self.naviko_visible = True
        self.naviko_flicker = 0

    def _notify(self, text):
        """画面上部に一時的な通知"""
        self.notification = text
        self.notification_timer = 60  # 2秒

    # ========== DRAW ==========

    def draw(self):
        pyxel.cls(COL_BLACK)

        if self.scene == SCENE_TITLE:
            self._draw_title()
        elif self.scene == SCENE_SELECT_AI:
            self._draw_select_ai()
        elif self.scene == SCENE_NAME_INPUT:
            self._draw_name_input()
        elif self.scene == SCENE_TUTORIAL:
            self._draw_tutorial()
        elif self.scene == SCENE_MAIN:
            self._draw_main()
        elif self.scene == SCENE_ROUTE_SELECT:
            self._draw_route_select()
        elif self.scene == SCENE_EVENT:
            self._draw_event()
        elif self.scene == SCENE_SHOP:
            self._draw_shop()

        # ナビ子オーバーレイ
        if self.naviko_visible:
            self._draw_naviko()

        # 通知オーバーレイ
        if self.notification:
            self._draw_notification()

    def _draw_title(self):
        for x in range(0, 256, 16):
            for y in range(0, 256, 16):
                if (x + y) % 32 == 0:
                    pyxel.rect(x, y, 16, 16, COL_DARK_BLUE)

        draw_text_center_shadow(60, "AUTOMATION EMPIRE", COL_YELLOW)
        draw_text_center_shadow(75, "- Jidouka Teikoku -", COL_LIGHT_GRAY)
        draw_text_center(100, "Clicker x AI x Side Hustle", COL_WHITE)

        if self.frame_count % 40 < 30:
            draw_text_center(160, "CLICK or ENTER to START", COL_PEACH)

        draw_text_center(230, "(c) 2026 SeANima", COL_DARK_GRAY)

    def _draw_select_ai(self):
        draw_text_center_shadow(10, "SELECT YOUR AI PARTNER", COL_YELLOW)
        draw_text_center(25, "Arrow keys: Move  Enter: Select", COL_LIGHT_GRAY)

        ai_info = [
            ("POEM", "Creator", COL_PINK),
            ("BUGMARU", "Tech", COL_BLUE),
            ("HATTARI", "Business", COL_ORANGE),
        ]

        for i, (name, role, col) in enumerate(ai_info):
            x, y = self.ai_positions[i]
            selected = i == self.selected_ai_index

            if selected:
                pyxel.rectb(x - 24, y - 24, 48, 64, COL_YELLOW)
                if self.frame_count % 20 < 15:
                    draw_text_center(y - 32, "v", COL_YELLOW)

            self._draw_ai_character(x, y, i, selected)

            name_x = x - len(name) * 2
            pyxel.text(name_x, y + 22, name, col if selected else COL_DARK_GRAY)
            role_x = x - len(role) * 2
            pyxel.text(role_x, y + 32, role, COL_WHITE if selected else COL_DARK_GRAY)

    def _draw_ai_character(self, cx, cy, ai_type, selected):
        """御三家のキャラクター描画"""
        col = AI_COLORS[ai_type] if selected else COL_DARK_GRAY
        accent = COL_WHITE if selected else COL_LIGHT_GRAY

        if ai_type == AI_POEM:
            pyxel.circ(cx, cy, 10, col)
            pyxel.circ(cx, cy, 8, COL_BLACK)
            pyxel.circ(cx, cy, 8, col)
            pyxel.rect(cx - 8, cy - 12, 16, 4, COL_BROWN)
            pyxel.rect(cx - 6, cy - 14, 12, 3, COL_BROWN)
            pyxel.pset(cx - 3, cy - 1, accent)
            pyxel.pset(cx + 3, cy - 1, accent)
            if selected and self.frame_count % 30 < 20:
                pyxel.pset(cx - 4, cy - 2, COL_YELLOW)
                pyxel.pset(cx + 4, cy - 2, COL_YELLOW)
            pyxel.pset(cx, cy + 3, accent)

        elif ai_type == AI_BUGMARU:
            pyxel.rect(cx - 9, cy - 9, 18, 18, col)
            pyxel.rectb(cx - 7, cy - 4, 6, 5, accent)
            pyxel.rectb(cx + 1, cy - 4, 6, 5, accent)
            pyxel.line(cx - 1, cy - 2, cx, cy - 2, accent)
            if selected:
                pyxel.line(cx + 5, cy - 4, cx + 7, cy - 6, COL_LIGHT_GRAY)
            pyxel.pset(cx - 4, cy - 2, COL_GREEN)
            pyxel.pset(cx + 3, cy - 2, COL_GREEN)
            pyxel.line(cx - 2, cy + 4, cx + 2, cy + 4, accent)

        elif ai_type == AI_HATTARI:
            pyxel.rect(cx - 6, cy - 10, 12, 20, col)
            pyxel.line(cx, cy - 6, cx - 3, cy + 2, COL_DARK_GRAY)
            pyxel.line(cx, cy - 6, cx + 3, cy + 2, COL_DARK_GRAY)
            pyxel.line(cx, cy - 5, cx, cy + 4, COL_RED)
            pyxel.line(cx - 4, cy - 3, cx - 2, cy - 3, accent)
            pyxel.line(cx + 2, cy - 3, cx + 4, cy - 3, accent)
            pyxel.pset(cx - 2, cy + 1, accent)
            pyxel.line(cx - 2, cy + 1, cx + 2, cy + 1, accent)
            pyxel.pset(cx + 3, cy, accent)
            pyxel.pset(cx - 3, cy, accent)

        pyxel.rect(cx - 5, cy + 10, 4, 4, col)
        pyxel.rect(cx + 1, cy + 10, 4, 4, col)

    def _draw_name_input(self):
        draw_text_center_shadow(40, "NAME YOUR AI", COL_YELLOW)
        draw_text_center(60, "Type a name (max 8 chars)", COL_LIGHT_GRAY)
        draw_text_center(72, "or press ENTER to keep default", COL_LIGHT_GRAY)

        box_w = 80
        box_x = (256 - box_w) // 2
        pyxel.rectb(box_x, 100, box_w, 16, COL_WHITE)
        text_x = box_x + 4
        pyxel.text(text_x, 105, self.name_input, COL_WHITE)

        if self.name_cursor_blink < 25:
            cursor_x = text_x + len(self.name_input) * 4
            pyxel.rect(cursor_x, 103, 1, 10, COL_WHITE)

        if self.ai_agent:
            self._draw_ai_character(128, 160, self.ai_agent.ai_type, True)
            draw_text_center(190, AI_TYPES[self.ai_agent.ai_type],
                             AI_COLORS[self.ai_agent.ai_type])

    def _draw_tutorial(self):
        pyxel.rect(0, 0, 256, 20, COL_DARK_BLUE)
        draw_text(4, 6, "TUTORIAL", COL_YELLOW)

        if self.tutorial_step < len(TUTORIAL_MESSAGES):
            msg = TUTORIAL_MESSAGES[self.tutorial_step]
            pyxel.rect(10, 80, 236, 60, COL_DARK_BLUE)
            pyxel.rectb(10, 80, 236, 60, COL_WHITE)
            draw_text(20, 90, msg, COL_WHITE)
            prog = f"{self.tutorial_step + 1}/{len(TUTORIAL_MESSAGES)}"
            pyxel.text(220, 130, prog, COL_DARK_GRAY)
            if self.frame_count % 40 < 30:
                draw_text_center(200, "CLICK to continue", COL_PEACH)

        self._draw_naviko_character(220, 70)

    def _draw_main(self):
        # ===== ヘッダー =====
        pyxel.rect(0, 0, 256, 24, COL_DARK_BLUE)

        coin_y = 4
        if self.coin_anim > 0:
            coin_y -= 1
        pyxel.circ(10, coin_y + 6, 5, COL_YELLOW)
        pyxel.circ(10, coin_y + 6, 3, COL_ORANGE)
        pyxel.text(9, coin_y + 4, "$", COL_YELLOW)

        coin_text = format_number(self.coins)
        pyxel.text(20, 4, coin_text, COL_YELLOW)

        auto = self._calc_auto_income()
        if auto > 0:
            pyxel.text(20, 14, f"+{format_number(auto)}/s", COL_GREEN)

        click_income = self._calc_click_income()
        pyxel.text(140, 4, f"Click:+{click_income}", COL_PEACH)

        # ===== ショップボタン =====
        pyxel.rect(200, 26, 52, 16, COL_DARK_GREEN)
        pyxel.rectb(200, 26, 52, 16, COL_GREEN)
        pyxel.text(206, 30, "SHOP[S]", COL_WHITE)

        # ===== AIパートナー表示 =====
        if self.ai_agent:
            pyxel.rect(0, 26, 198, 30, COL_BLACK)
            pyxel.rectb(0, 26, 198, 30, COL_DARK_GRAY)

            self._draw_ai_character(20, 40, self.ai_agent.ai_type, True)

            pyxel.text(38, 30, self.ai_agent.name,
                       AI_COLORS[self.ai_agent.ai_type])

            # ルート表示
            info = f"Lv.{self.ai_agent.level}"
            if self.ai_agent.route != ROUTE_NONE:
                info += f" {ROUTE_NAMES[self.ai_agent.route]}"
            pyxel.text(38, 38, info, COL_WHITE)

            # 経験値バー
            bar_x, bar_y, bar_w = 38, 48, 80
            pyxel.rect(bar_x, bar_y, bar_w, 4, COL_DARK_GRAY)
            fill_w = int(bar_w * self.ai_agent.exp_progress)
            if fill_w > 0:
                pyxel.rect(bar_x, bar_y, fill_w, 4, COL_GREEN)

            if self.ai_agent.level >= 10:
                pyxel.text(bar_x + bar_w + 4, bar_y - 1, "MAX", COL_YELLOW)
            else:
                pyxel.text(bar_x + bar_w + 4, bar_y - 1,
                           f"{self.ai_agent.exp}/{self.ai_agent.exp_to_next}",
                           COL_LIGHT_GRAY)

        # ===== クリックエリア =====
        center_x, center_y = 128, 130
        pulse = abs(self.frame_count % 30 - 15)
        r = 20 + pulse // 5
        pyxel.circ(center_x, center_y, r, COL_YELLOW)
        pyxel.circ(center_x, center_y, r - 3, COL_ORANGE)
        pyxel.circ(center_x, center_y, r - 6, COL_YELLOW)
        draw_text_center_shadow(center_y - 3, "$", COL_WHITE)

        if self.frame_count % 60 < 45:
            draw_text_center(center_y + r + 8, "CLICK!", COL_PEACH)

        # ===== 副業リスト =====
        owned = self.job_mgr.get_owned_jobs()
        panel_y = 195
        panel_h = 256 - panel_y
        pyxel.rect(0, panel_y, 256, panel_h, COL_DARK_BLUE)
        pyxel.rectb(0, panel_y, 256, panel_h, COL_LIGHT_GRAY)
        pyxel.text(4, panel_y + 3, f"GIGS ({len(owned)})", COL_YELLOW)

        for i, job in enumerate(owned):
            if i >= 4:
                pyxel.text(4, panel_y + 13 + i * 10, "...", COL_DARK_GRAY)
                break
            y = panel_y + 13 + i * 10
            active = job["id"] in self.job_mgr.active_jobs
            col = COL_GREEN if active else COL_DARK_GRAY
            route_mark = ""
            if job["route"] is not None:
                route_mark = ROUTE_ICONS[job["route"]] + " "
            pyxel.text(8, y, f"> {route_mark}{job['name']}", col)
            pyxel.text(180, y, f"+{job['base_income']}/c", col)

        # ===== クリックエフェクト =====
        for e in self.click_effects:
            alpha = e["timer"] / 20
            col = COL_YELLOW if alpha > 0.5 else COL_ORANGE
            pyxel.text(int(e["x"]) - 8, int(e["y"]), e["text"], col)

    def _draw_route_select(self):
        """ルート選択画面"""
        draw_text_center_shadow(10, "CHOOSE YOUR ROUTE", COL_YELLOW)
        draw_text_center(25, "This shapes your empire!", COL_LIGHT_GRAY)

        routes = [
            ("CREATOR", "Art/Writing/Video", COL_PINK, "Art"),
            ("TECH", "Code/Apps/Bots", COL_BLUE, "Code"),
            ("BUSINESS", "Sales/Marketing", COL_ORANGE, "Biz"),
        ]

        positions = [(40, 100), (128, 100), (216, 100)]

        for i, (name, desc, col, icon) in enumerate(routes):
            x, y = positions[i]
            selected = i == self.route_cursor

            # 枠
            if selected:
                pyxel.rectb(x - 30, y - 20, 60, 50, COL_YELLOW)
                if self.frame_count % 20 < 15:
                    pyxel.text(x - 2, y - 28, "v", COL_YELLOW)
            else:
                pyxel.rectb(x - 30, y - 20, 60, 50, COL_DARK_GRAY)

            # アイコン（簡易）
            pyxel.rect(x - 8, y - 8, 16, 16, col if selected else COL_DARK_GRAY)
            icon_x = x - len(icon) * 2
            pyxel.text(icon_x, y - 2, icon, COL_WHITE if selected else COL_BLACK)

            # 名前
            nx = x - len(name) * 2
            pyxel.text(nx, y + 14, name, col if selected else COL_DARK_GRAY)

            # 説明
            dx = x - len(desc) * 2
            pyxel.text(dx, y + 24, desc, COL_WHITE if selected else COL_DARK_GRAY)

            # 適性マーク
            if self.ai_agent and i == self.ai_agent.aptitude_route:
                pyxel.text(x + 20, y - 18, "*", COL_YELLOW)

        # 適性ヒント
        if self.ai_agent:
            apt_name = ROUTE_NAMES[self.ai_agent.aptitude_route]
            draw_text_center(170, f"* = {self.ai_agent.name}'s strength ({apt_name})",
                             COL_YELLOW)

        draw_text_center(190, "Arrow keys: Move  Enter: Select", COL_LIGHT_GRAY)

    def _draw_event(self):
        """やらかしイベント画面"""
        if not self.current_event:
            return

        # 背景を暗く
        pyxel.rect(0, 0, 256, 256, COL_BLACK)

        # 警告ヘッダー
        if self.frame_count % 20 < 15:
            pyxel.rect(0, 0, 256, 20, COL_RED)
            draw_text_center(6, "!! INCIDENT !!", COL_WHITE)
        else:
            pyxel.rect(0, 0, 256, 20, COL_DARK_PURPLE)
            draw_text_center(6, "!! INCIDENT !!", COL_RED)

        # タイトル
        draw_text_center_shadow(30, self.current_event["title"], COL_YELLOW)

        # AIキャラ（動揺してる感じ）
        if self.ai_agent:
            shake_x = (self.frame_count % 4) - 2
            self._draw_ai_character(
                128 + shake_x, 60, self.ai_agent.ai_type, True
            )

        # 説明文
        desc = self.current_event["desc"].format(
            name=self.ai_agent.name if self.ai_agent else "AI"
        )
        pyxel.rect(20, 90, 216, 50, COL_DARK_BLUE)
        pyxel.rectb(20, 90, 216, 50, COL_BLUE)
        draw_text(30, 98, desc, COL_WHITE)

        if self.event_result:
            # 結果表示
            result = self.event_result
            result_col = COL_GREEN if result["result"] == "good" else (
                COL_RED if result["result"] == "bad" else COL_YELLOW
            )
            pyxel.rect(20, 150, 216, 60, COL_DARK_BLUE)
            pyxel.rectb(20, 150, 216, 60, result_col)

            result_msg = result["msg"].format(
                name=self.ai_agent.name if self.ai_agent else "AI"
            )
            draw_text(30, 158, result_msg, COL_WHITE)

            # コイン変化
            effect = result["coin_effect"]
            if effect != 0:
                effect_text = f"{effect:+d} coins"
                effect_col = COL_GREEN if effect > 0 else COL_RED
                pyxel.text(30, 195, effect_text, effect_col)

            if self.frame_count % 40 < 30:
                draw_text_center(220, "CLICK to continue", COL_PEACH)
        else:
            # 選択肢表示
            choices = self.current_event["choices"]
            for i, choice in enumerate(choices):
                y = 160 + i * 20
                selected = i == self.event_choice_cursor
                if selected:
                    pyxel.rect(30, y - 2, 196, 14, COL_DARK_PURPLE)
                    pyxel.rectb(30, y - 2, 196, 14, COL_YELLOW)
                    pyxel.text(36, y + 1, f"> {choice['text']}", COL_WHITE)
                else:
                    pyxel.rectb(30, y - 2, 196, 14, COL_DARK_GRAY)
                    pyxel.text(36, y + 1, f"  {choice['text']}", COL_LIGHT_GRAY)

            draw_text_center(220, "Up/Down: Move  Enter: Select", COL_LIGHT_GRAY)

    def _draw_shop(self):
        """ショップ画面"""
        pyxel.rect(0, 0, 256, 256, COL_BLACK)

        # ヘッダー
        pyxel.rect(0, 0, 256, 24, COL_DARK_GREEN)
        draw_text_center(4, "SIDE HUSTLE SHOP", COL_WHITE)
        pyxel.text(4, 14, f"Coins: {format_number(self.coins)}", COL_YELLOW)
        pyxel.text(180, 14, "[S]/[ESC]:Back", COL_LIGHT_GRAY)

        # ルート表示
        if self.ai_agent and self.ai_agent.route != ROUTE_NONE:
            route_name = ROUTE_NAMES[self.ai_agent.route]
            pyxel.text(100, 30, f"Route: {route_name}",
                       ROUTE_COLORS[self.ai_agent.route])
        elif self.ai_agent:
            pyxel.text(100, 30, "Route: Not selected", COL_DARK_GRAY)

        if not self.shop_items:
            draw_text_center(100, "No new gigs available!", COL_LIGHT_GRAY)
            draw_text_center(115, "Level up to unlock more.", COL_DARK_GRAY)
            return

        # アイテムリスト
        max_visible = 8
        start = max(0, self.shop_cursor - max_visible + 1)
        end = min(len(self.shop_items), start + max_visible)

        for idx in range(start, end):
            job = self.shop_items[idx]
            display_i = idx - start
            y = 45 + display_i * 24
            selected = idx == self.shop_cursor
            can_afford = self.coins >= job["cost"]

            # 背景
            if selected:
                pyxel.rect(4, y - 2, 248, 22, COL_DARK_BLUE)
                pyxel.rectb(4, y - 2, 248, 22, COL_YELLOW)
            else:
                pyxel.rectb(4, y - 2, 248, 22, COL_DARK_GRAY)

            # ルートマーク
            if job["route"] is not None:
                rc = ROUTE_COLORS[job["route"]]
                pyxel.text(10, y + 2, ROUTE_ICONS[job["route"]], rc)
                name_x = 30
            else:
                name_x = 10

            # 名前
            name_col = COL_WHITE if can_afford else COL_DARK_GRAY
            pyxel.text(name_x, y + 2, job["name"], name_col)

            # レベル
            pyxel.text(name_x, y + 10, f"Lv{job['level']}", COL_DARK_GRAY)

            # 収入
            pyxel.text(140, y + 2, f"+{job['base_income']}/c",
                       COL_GREEN if can_afford else COL_DARK_GRAY)

            # 価格
            cost_text = format_number(job["cost"])
            cost_col = COL_YELLOW if can_afford else COL_RED
            pyxel.text(200, y + 2, f"${cost_text}", cost_col)

        # 説明（選択中の副業）
        if self.shop_cursor < len(self.shop_items):
            selected_job = self.shop_items[self.shop_cursor]
            desc_y = 240
            pyxel.rect(0, desc_y - 4, 256, 20, COL_DARK_BLUE)
            pyxel.text(8, desc_y, selected_job["desc"], COL_LIGHT_GRAY)

    def _draw_naviko(self):
        """ナビ子のメッセージウィンドウ"""
        if not self.naviko_msg:
            return

        win_y = 180
        win_h = 55

        offset_x = 0
        if self.naviko_flicker == 30:
            offset_x = 2
        elif self.naviko_flicker == 31:
            offset_x = -1

        pyxel.rect(8 + offset_x, win_y, 240, win_h, COL_DARK_BLUE)
        pyxel.rectb(8 + offset_x, win_y, 240, win_h, COL_BLUE)

        self._draw_naviko_character(24 + offset_x, win_y + 12)

        pyxel.text(38 + offset_x, win_y + 4, "NAVIKO", COL_BLUE)
        draw_text(38 + offset_x, win_y + 14, self.naviko_msg, COL_WHITE)

        if self.naviko_timer == 0 and self.frame_count % 40 < 30:
            pyxel.text(200, win_y + win_h - 10, ">", COL_PEACH)

    def _draw_naviko_character(self, x, y):
        """ナビ子描画（ホログラム型）"""
        glitch = self.naviko_flicker in (30, 31)
        body_col = COL_BLUE if not glitch else COL_INDIGO
        glow_col = COL_LIGHT_GRAY

        pyxel.rect(x - 4, y, 8, 10, body_col)
        pyxel.circ(x, y - 2, 4, body_col)
        pyxel.line(x + 1, y - 6, x + 3, y - 10, COL_BLUE)
        pyxel.pset(x + 3, y - 11, COL_PEACH)

        for i in range(5):
            px = x - 3 + (self.frame_count * 2 + i * 7) % 7
            py = y + 10 + i * 2
            if (self.frame_count + i * 3) % 4 != 0:
                pyxel.pset(px, py, glow_col)

        pyxel.pset(x - 2, y - 2, COL_WHITE)
        pyxel.pset(x + 2, y - 2, COL_WHITE)

        if glitch:
            pyxel.rect(x - 4 + 2, y + 1, 8, 10, COL_INDIGO)

    def _draw_notification(self):
        """画面上部の一時通知"""
        w = len(self.notification) * 4 + 16
        x = (256 - w) // 2
        pyxel.rect(x, 58, w, 12, COL_DARK_PURPLE)
        pyxel.rectb(x, 58, w, 12, COL_YELLOW)
        pyxel.text(x + 8, 60, self.notification, COL_YELLOW)
