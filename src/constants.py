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

AI_NAMES_DEFAULT = ["Poem", "Bugmaru", "Hattari"]
AI_TYPES = ["Creator", "Tech", "Business"]
AI_COLORS = [COL_PINK, COL_BLUE, COL_ORANGE]

# 副業レベル
JOB_LV1 = [
    {"name": "Data Entry", "base_income": 1, "desc": "Your first income. Click basics."},
    {"name": "Survey Writing", "base_income": 2, "desc": "Improves click efficiency."},
    {"name": "Research Assistant", "base_income": 3, "desc": "Gain info resources."},
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
    "Hey, nice to meet you.\nI'm Naviko.",
    "This is 'Automation Empire'.\nTeam up with AI and grind\nyour side hustle.",
    "First, click the screen\nand earn some coins.",
    "...Oh wait, right.\nYou need to pick an AI\nto be your partner.",
    "Three to choose from,\nbut they're all garbage.\nJust pick one you like.",
]

# ナビ子のセリフ集
NAVIKO_LINES = {
    "select_intro": "Alright, meet the Big Three.\nThey're all disasters,\nbut pick your favorite.",
    "poem_desc": "Poem. Creator type.\nSensitivity goes haywire.\nWatch out for poetry in deliverables.",
    "bugmaru_desc": "Bugmaru. Tech type.\nHard worker, but sloppy.\nDelivers bugs with confidence.",
    "hattari_desc": "Hattari. Business type.\nMaster talker. Silver tongue.\nAlways rounds numbers up.",
    "selected": "...{name}, huh. Sure, good luck.\nI'll cover for you.",
    "tutorial_click": "Click the screen\nand earn some coins.\n{name} will help... probably.",
    "first_job": "Unlocked your first gig:\n'Data Entry'.\nLeave it to {name}.",
}
