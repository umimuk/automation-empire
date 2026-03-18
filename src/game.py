"""メインゲームクラス - 自動化帝国"""

import pyxel
from src.constants import *
from src.ai_agent import AIAgent
from src.text_util import (
    draw_text, draw_text_center, draw_text_shadow,
    draw_text_center_shadow, format_number,
)


class Game:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="Automation Empire", fps=FPS)

        # ゲーム状態
        self.scene = SCENE_TITLE
        self.coins = 0
        self.total_coins = 0
        self.click_power = BASE_CLICK_INCOME
        self.ai_agent = None  # 選択後に設定
        self.frame_count = 0

        # UI状態
        self.selected_ai_index = 0  # 御三家選択カーソル
        self.tutorial_step = 0
        self.msg_timer = 0  # メッセージ表示タイマー
        self.click_effects = []  # クリックエフェクト [{x, y, text, timer}]
        self.coin_anim = 0  # コイン表示アニメーション

        # 御三家描画位置
        self.ai_positions = [
            (40, 120),   # 左：ポエム
            (108, 120),  # 中：バグ丸
            (176, 120),  # 右：ハッタリ
        ]

        # 名前入力
        self.name_input = ""
        self.name_cursor_blink = 0

        # ナビ子
        self.naviko_msg = ""
        self.naviko_timer = 0
        self.naviko_visible = False
        self.naviko_flicker = 0  # ホログラムノイズ演出

        # メイン画面
        self.auto_income_timer = 0
        self.jobs_unlocked = []
        self.tutorial_done = False

        # 副業
        self.active_jobs = []  # 稼働中の副業

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

    def _update_title(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_SELECT_AI
            self._show_naviko(NAVIKO_LINES["select_intro"], 0)

    def _update_select_ai(self):
        # 左右キーで選択
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.selected_ai_index = (self.selected_ai_index - 1) % 3
            self._show_ai_description()
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.selected_ai_index = (self.selected_ai_index + 1) % 3
            self._show_ai_description()

        # マウスクリックで選択
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            for i, (ax, ay) in enumerate(self.ai_positions):
                if ax - 20 <= mx <= ax + 20 and ay - 20 <= my <= ay + 20:
                    self.selected_ai_index = i
                    self._show_ai_description()
                    break

        # 決定
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_SPACE):
            self.ai_agent = AIAgent(self.selected_ai_index)
            self.name_input = self.ai_agent.name
            self.scene = SCENE_NAME_INPUT

    def _show_ai_description(self):
        descs = ["poem_desc", "bugmaru_desc", "hattari_desc"]
        self._show_naviko(NAVIKO_LINES[descs[self.selected_ai_index]], 0)

    def _update_name_input(self):
        self.name_cursor_blink = (self.name_cursor_blink + 1) % 40

        # テキスト入力（ASCII文字のみ）
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
                # 最初の副業をアンロック
                self.jobs_unlocked = [0]  # データ入力
                self.active_jobs = [0]
                msg = NAVIKO_LINES["tutorial_click"].format(
                    name=self.ai_agent.name
                )
                self._show_naviko(msg, 150)

    def _update_main(self):
        # クリック処理
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            # クリックエリア判定（画面中央〜下部）
            if 30 <= my <= 200:
                income = self._calc_click_income()
                self.coins += income
                self.total_coins += income
                self.coin_anim = 10

                # AIに経験値
                if self.ai_agent:
                    leveled = self.ai_agent.add_exp(AI_EXP_PER_CLICK)
                    if leveled:
                        self._show_naviko(
                            f"{self.ai_agent.name} Lv{self.ai_agent.level}!",
                            90,
                        )

                # クリックエフェクト
                self.click_effects.append({
                    "x": mx, "y": my,
                    "text": f"+{format_number(income)}",
                    "timer": 20,
                })

        # 自動収入（1秒ごと）
        self.auto_income_timer += 1
        if self.auto_income_timer >= FPS:
            self.auto_income_timer = 0
            if self.ai_agent and self.active_jobs:
                auto = self._calc_auto_income()
                if auto > 0:
                    self.coins += auto
                    self.total_coins += auto

        # コインアニメーション
        if self.coin_anim > 0:
            self.coin_anim -= 1

    def _calc_click_income(self):
        """クリック収入を計算"""
        base = self.click_power
        # 稼働中の副業のボーナス
        for job_id in self.active_jobs:
            base += JOB_LV1[job_id]["base_income"]
        return base

    def _calc_auto_income(self):
        """自動収入を計算（1秒あたり）"""
        if not self.ai_agent:
            return 0
        return int(self.ai_agent.auto_income * len(self.active_jobs))

    def _show_naviko(self, msg, duration=0):
        """ナビ子のメッセージを表示（duration=0で手動消し）"""
        self.naviko_msg = msg
        self.naviko_timer = duration
        self.naviko_visible = True
        self.naviko_flicker = 0  # ノイズリセット

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

        # ナビ子オーバーレイ（全画面共通）
        if self.naviko_visible:
            self._draw_naviko()

    def _draw_title(self):
        # 背景のグリッドパターン
        for x in range(0, 256, 16):
            for y in range(0, 256, 16):
                if (x + y) % 32 == 0:
                    pyxel.rect(x, y, 16, 16, COL_DARK_BLUE)

        # タイトル
        draw_text_center_shadow(60, "AUTOMATION EMPIRE", COL_YELLOW)
        draw_text_center_shadow(75, "- Jidouka Teikoku -", COL_LIGHT_GRAY)

        # サブタイトル
        draw_text_center(100, "Clicker x AI x Side Hustle", COL_WHITE)

        # 点滅テキスト
        if self.frame_count % 40 < 30:
            draw_text_center(160, "CLICK or ENTER to START", COL_PEACH)

        # クレジット
        draw_text_center(230, "(c) 2026 SeANima", COL_DARK_GRAY)

    def _draw_select_ai(self):
        # ヘッダー
        draw_text_center_shadow(10, "SELECT YOUR AI PARTNER", COL_YELLOW)
        draw_text_center(25, "Arrow keys: Move  Enter: Select", COL_LIGHT_GRAY)

        # 御三家描画
        ai_info = [
            ("POEM", "Creator", COL_PINK),
            ("BUGMARU", "Tech", COL_BLUE),
            ("HATTARI", "Business", COL_ORANGE),
        ]

        for i, (name, role, col) in enumerate(ai_info):
            x, y = self.ai_positions[i]
            selected = i == self.selected_ai_index

            # 選択枠
            if selected:
                border_col = COL_YELLOW
                pyxel.rectb(x - 24, y - 24, 48, 64, border_col)
                # 選択マーカー
                if self.frame_count % 20 < 15:
                    draw_text_center(y - 32, "v", COL_YELLOW)
            else:
                border_col = COL_DARK_GRAY

            # キャラクター（簡易ドット絵）
            self._draw_ai_character(x, y, i, selected)

            # 名前
            name_x = x - len(name) * 2
            pyxel.text(name_x, y + 22, name, col if selected else COL_DARK_GRAY)

            # 適性
            role_x = x - len(role) * 2
            pyxel.text(role_x, y + 32, role,
                       COL_WHITE if selected else COL_DARK_GRAY)

    def _draw_ai_character(self, cx, cy, ai_type, selected):
        """御三家のキャラクター描画（簡易ドット絵）"""
        col = AI_COLORS[ai_type] if selected else COL_DARK_GRAY
        accent = COL_WHITE if selected else COL_LIGHT_GRAY

        if ai_type == AI_POEM:  # ポエム：丸っこい
            # 体（丸）
            pyxel.circ(cx, cy, 10, col)
            pyxel.circ(cx, cy, 8, COL_BLACK)
            pyxel.circ(cx, cy, 8, col)
            # ベレー帽
            pyxel.rect(cx - 8, cy - 12, 16, 4, COL_BROWN)
            pyxel.rect(cx - 6, cy - 14, 12, 3, COL_BROWN)
            # 目（キラキラ）
            pyxel.pset(cx - 3, cy - 1, accent)
            pyxel.pset(cx + 3, cy - 1, accent)
            if selected and self.frame_count % 30 < 20:
                pyxel.pset(cx - 4, cy - 2, COL_YELLOW)
                pyxel.pset(cx + 4, cy - 2, COL_YELLOW)
            # 口
            pyxel.pset(cx, cy + 3, accent)

        elif ai_type == AI_BUGMARU:  # バグ丸：角張った
            # 体（四角）
            pyxel.rect(cx - 9, cy - 9, 18, 18, col)
            # メガネ
            pyxel.rectb(cx - 7, cy - 4, 6, 5, accent)
            pyxel.rectb(cx + 1, cy - 4, 6, 5, accent)
            pyxel.line(cx - 1, cy - 2, cx, cy - 2, accent)
            # ヒビ
            if selected:
                pyxel.line(cx + 5, cy - 4, cx + 7, cy - 6, COL_LIGHT_GRAY)
            # 目
            pyxel.pset(cx - 4, cy - 2, COL_GREEN)
            pyxel.pset(cx + 3, cy - 2, COL_GREEN)
            # 口（真一文字）
            pyxel.line(cx - 2, cy + 4, cx + 2, cy + 4, accent)

        elif ai_type == AI_HATTARI:  # ハッタリ：スリム
            # 体（スリム長方形）
            pyxel.rect(cx - 6, cy - 10, 12, 20, col)
            # スーツ感（Vライン）
            pyxel.line(cx, cy - 6, cx - 3, cy + 2, COL_DARK_GRAY)
            pyxel.line(cx, cy - 6, cx + 3, cy + 2, COL_DARK_GRAY)
            # ネクタイ
            pyxel.line(cx, cy - 5, cx, cy + 4, COL_RED)
            # 目（細め）
            pyxel.line(cx - 4, cy - 3, cx - 2, cy - 3, accent)
            pyxel.line(cx + 2, cy - 3, cx + 4, cy - 3, accent)
            # 口角上がり
            pyxel.pset(cx - 2, cy + 1, accent)
            pyxel.line(cx - 2, cy + 1, cx + 2, cy + 1, accent)
            pyxel.pset(cx + 3, cy, accent)
            pyxel.pset(cx - 3, cy, accent)

        # 足（共通）
        pyxel.rect(cx - 5, cy + 10, 4, 4, col)
        pyxel.rect(cx + 1, cy + 10, 4, 4, col)

    def _draw_name_input(self):
        draw_text_center_shadow(40, "NAME YOUR AI", COL_YELLOW)
        draw_text_center(60, "Type a name (max 8 chars)", COL_LIGHT_GRAY)
        draw_text_center(72, "or press ENTER to keep default", COL_LIGHT_GRAY)

        # 入力ボックス
        box_w = 80
        box_x = (256 - box_w) // 2
        pyxel.rectb(box_x, 100, box_w, 16, COL_WHITE)

        # 入力テキスト
        text_x = box_x + 4
        pyxel.text(text_x, 105, self.name_input, COL_WHITE)

        # カーソル
        if self.name_cursor_blink < 25:
            cursor_x = text_x + len(self.name_input) * 4
            pyxel.rect(cursor_x, 103, 1, 10, COL_WHITE)

        # 選んだAIの表示
        if self.ai_agent:
            self._draw_ai_character(128, 160, self.ai_agent.ai_type, True)
            draw_text_center(190, AI_TYPES[self.ai_agent.ai_type],
                             AI_COLORS[self.ai_agent.ai_type])

    def _draw_tutorial(self):
        # 背景（メイン画面のプレビュー的な）
        pyxel.rect(0, 0, 256, 20, COL_DARK_BLUE)
        draw_text(4, 6, "TUTORIAL", COL_YELLOW)

        # チュートリアルメッセージ
        if self.tutorial_step < len(TUTORIAL_MESSAGES):
            msg = TUTORIAL_MESSAGES[self.tutorial_step]

            # メッセージウィンドウ
            pyxel.rect(10, 80, 236, 60, COL_DARK_BLUE)
            pyxel.rectb(10, 80, 236, 60, COL_WHITE)

            draw_text(20, 90, msg, COL_WHITE)

            # 進捗
            prog = f"{self.tutorial_step + 1}/{len(TUTORIAL_MESSAGES)}"
            pyxel.text(220, 130, prog, COL_DARK_GRAY)

            # 続行指示
            if self.frame_count % 40 < 30:
                draw_text_center(200, "CLICK to continue", COL_PEACH)

        # ナビ子表示（チュートリアル中は常時）
        self._draw_naviko_character(220, 70)

    def _draw_main(self):
        # ===== ヘッダー（資産表示） =====
        pyxel.rect(0, 0, 256, 24, COL_DARK_BLUE)

        # コインアイコン
        coin_y = 4
        if self.coin_anim > 0:
            coin_y -= 1  # バウンス
        pyxel.circ(10, coin_y + 6, 5, COL_YELLOW)
        pyxel.circ(10, coin_y + 6, 3, COL_ORANGE)
        pyxel.text(9, coin_y + 4, "$", COL_YELLOW)

        # コイン数
        coin_text = format_number(self.coins)
        pyxel.text(20, 4, coin_text, COL_YELLOW)

        # 自動収入表示
        auto = self._calc_auto_income()
        if auto > 0:
            pyxel.text(20, 14, f"+{format_number(auto)}/s", COL_GREEN)

        # クリック力表示
        click_income = self._calc_click_income()
        pyxel.text(180, 4, f"Click: +{click_income}", COL_PEACH)

        # ===== AIパートナー表示 =====
        if self.ai_agent:
            # AI情報パネル
            pyxel.rect(0, 26, 256, 30, COL_BLACK)
            pyxel.rectb(0, 26, 256, 30, COL_DARK_GRAY)

            # AIキャラ小さめ
            self._draw_ai_character(20, 40, self.ai_agent.ai_type, True)

            # 名前とレベル
            pyxel.text(38, 30, self.ai_agent.name, AI_COLORS[self.ai_agent.ai_type])
            pyxel.text(38, 38, f"Lv.{self.ai_agent.level} {self.ai_agent.type_name}",
                       COL_WHITE)

            # 経験値バー
            bar_x, bar_y, bar_w = 38, 48, 100
            pyxel.rect(bar_x, bar_y, bar_w, 4, COL_DARK_GRAY)
            fill_w = int(bar_w * self.ai_agent.exp_progress)
            if fill_w > 0:
                pyxel.rect(bar_x, bar_y, fill_w, 4, COL_GREEN)
            pyxel.text(bar_x + bar_w + 4, bar_y - 1,
                       f"{self.ai_agent.exp}/{self.ai_agent.exp_to_next}",
                       COL_LIGHT_GRAY)

        # ===== クリックエリア =====
        click_area_y = 60
        # クリック誘導（中央のコイン）
        center_x, center_y = 128, 140
        pulse = abs(self.frame_count % 30 - 15)
        r = 20 + pulse // 5
        pyxel.circ(center_x, center_y, r, COL_YELLOW)
        pyxel.circ(center_x, center_y, r - 3, COL_ORANGE)
        pyxel.circ(center_x, center_y, r - 6, COL_YELLOW)
        draw_text_center_shadow(center_y - 3, "$", COL_WHITE)

        # クリック指示
        if self.frame_count % 60 < 45:
            draw_text_center(center_y + r + 8, "CLICK!", COL_PEACH)

        # ===== 副業リスト =====
        pyxel.rect(0, 205, 256, 51, COL_DARK_BLUE)
        pyxel.rectb(0, 205, 256, 51, COL_LIGHT_GRAY)
        pyxel.text(4, 208, "SIDE HUSTLES", COL_YELLOW)

        for i, job_id in enumerate(self.jobs_unlocked):
            job = JOB_LV1[job_id]
            y = 218 + i * 10
            active = job_id in self.active_jobs
            col = COL_GREEN if active else COL_DARK_GRAY
            marker = ">" if active else " "
            pyxel.text(8, y, f"{marker} {job['name']}", col)
            pyxel.text(160, y, f"+{job['base_income']}/click", col)

        # ===== クリックエフェクト =====
        for e in self.click_effects:
            alpha = e["timer"] / 20
            col = COL_YELLOW if alpha > 0.5 else COL_ORANGE
            pyxel.text(int(e["x"]) - 8, int(e["y"]), e["text"], col)

    def _draw_naviko(self):
        """ナビ子のメッセージウィンドウ（ホログラム演出付き）"""
        if not self.naviko_msg:
            return

        # メッセージウィンドウ（画面下部）
        win_y = 180
        win_h = 55

        # ホログラムノイズ: たまにウィンドウが一瞬ずれる
        offset_x = 0
        if self.naviko_flicker == 30:
            offset_x = 2  # ノイズでズレる
        elif self.naviko_flicker == 31:
            offset_x = -1

        pyxel.rect(8 + offset_x, win_y, 240, win_h, COL_DARK_BLUE)
        pyxel.rectb(8 + offset_x, win_y, 240, win_h, COL_BLUE)

        # ナビ子アイコン
        self._draw_naviko_character(24 + offset_x, win_y + 12)

        # 名前ラベル
        pyxel.text(38 + offset_x, win_y + 4, "NAVIKO", COL_BLUE)

        # メッセージテキスト
        draw_text(38 + offset_x, win_y + 14, self.naviko_msg, COL_WHITE)

        # 続行指示（自動消去じゃない場合）
        if self.naviko_timer == 0 and self.frame_count % 40 < 30:
            pyxel.text(200, win_y + win_h - 10, ">", COL_PEACH)

    def _draw_naviko_character(self, x, y):
        """ナビ子描画（ホログラム型）"""
        # ホログラムノイズ判定
        glitch = self.naviko_flicker in (30, 31)

        # 基本色（半透明感を色で表現）
        body_col = COL_BLUE if not glitch else COL_INDIGO
        glow_col = COL_LIGHT_GRAY

        # 上半身（シルエット）
        pyxel.rect(x - 4, y, 8, 10, body_col)
        # 頭
        pyxel.circ(x, y - 2, 4, body_col)
        # アホ毛（アンテナ）
        pyxel.line(x + 1, y - 6, x + 3, y - 10, COL_BLUE)
        pyxel.pset(x + 3, y - 11, COL_PEACH)  # 先端光る

        # 下半身（光の粒子に溶ける）
        for i in range(5):
            px = x - 3 + (self.frame_count * 2 + i * 7) % 7
            py = y + 10 + i * 2
            if (self.frame_count + i * 3) % 4 != 0:  # 点滅
                pyxel.pset(px, py, glow_col)

        # 目
        pyxel.pset(x - 2, y - 2, COL_WHITE)
        pyxel.pset(x + 2, y - 2, COL_WHITE)

        # グリッチ時：二重表示
        if glitch:
            pyxel.rect(x - 4 + 2, y + 1, 8, 10, COL_INDIGO)
