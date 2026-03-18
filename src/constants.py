"""ゲーム定数"""

# 画面サイズ
SCREEN_W = 256
SCREEN_H = 256
FPS = 30

# 色定数（Pyxel 16色パレット）
COL_BLACK = 0
COL_DARK_BLUE = 1
COL_DARK_PURPLE = 2
COL_DARK_GREEN = 3
COL_BROWN = 4
COL_DARK_GRAY = 5
COL_LIGHT_GRAY = 6
COL_WHITE = 7
COL_RED = 8
COL_ORANGE = 9
COL_YELLOW = 10
COL_GREEN = 11
COL_BLUE = 12
COL_INDIGO = 13
COL_PINK = 14
COL_PEACH = 15

# ゲーム画面状態
SCENE_TITLE = 0
SCENE_SELECT_AI = 1
SCENE_NAME_INPUT = 2
SCENE_TUTORIAL = 3
SCENE_MAIN = 4
SCENE_EVENT = 5
SCENE_MENU = 6

# 御三家タイプ
AI_POEM = 0     # ポエム（クリエイター適性）
AI_BUGMARU = 1  # バグ丸（テック適性）
AI_HATTARI = 2  # ハッタリ（ビジネス適性）

AI_NAMES_DEFAULT = ["ポエム", "バグ丸", "ハッタリ"]
AI_TYPES = ["クリエイター", "テック", "ビジネス"]
AI_COLORS = [COL_PINK, COL_BLUE, COL_ORANGE]

# 副業レベル
JOB_LV1 = [
    {"name": "データ入力", "base_income": 1, "desc": "最初の収入源。クリックの基本"},
    {"name": "アンケート代筆", "base_income": 2, "desc": "クリック効率UP"},
    {"name": "リサーチ代行", "base_income": 3, "desc": "情報リソース獲得"},
]

# クリック基本収入
BASE_CLICK_INCOME = 1

# AI成長パラメータ
AI_BASE_EFFICIENCY = 0.1   # Lv1の自動収入倍率
AI_GROWTH_RATE = 0.15      # レベルごとの効率上昇
AI_EXP_PER_CLICK = 1       # クリックあたりの経験値
AI_EXP_CURVE = [0, 10, 30, 60, 100, 150, 210, 280, 360, 450, 999999]  # Lv1-10+の経験値テーブル

# やらかし確率（Lv1=高い、成長で減る）
INCIDENT_BASE_CHANCE = 0.05  # 5%/秒
INCIDENT_LV_REDUCTION = 0.005  # レベルあたり-0.5%

# チュートリアルメッセージ
TUTORIAL_MESSAGES = [
    "やぁ、初めまして。\nナビ子だよ。",
    "ここは「自動化帝国」。\nAIと一緒に副業して\n稼ぐゲームだよ。",
    "まずは画面をクリックして\nコインを稼いでみて。",
    "…あ、その前に。\nあなたの相棒になるAIを\n選んでもらうんだった。",
    "3体いるけど、\nどれもポンコツだから\nまあ好きなの選んで。",
]

# ナビ子のセリフ集
NAVIKO_LINES = {
    "select_intro": "さて、こいつらが御三家。\nどれもポンコツだけど\n好きなの選んで。",
    "poem_desc": "ポエム。クリエイター適性。\n感性が暴走するタイプ。\n納品物にポエム混入注意。",
    "bugmaru_desc": "バグ丸。テック適性。\n真面目だけど詰めが甘い。\n自信満々にバグ納品する。",
    "hattari_desc": "ハッタリ。ビジネス適性。\nコミュ力おばけ。口が上手い。\n数字は盛る方向で丸める。",
    "selected": "…{name}ね。まあ、頑張って。\n私がフォローするから。",
    "tutorial_click": "画面をクリックして\nコインを稼いでみて。\n{name}も手伝う…はず。",
    "first_job": "最初の副業「データ入力」を\nアンロックしたよ。\n{name}に任せてみて。",
}
