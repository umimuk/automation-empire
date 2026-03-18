"""Game constants and data definitions."""

# Screen
WIDTH = 240
HEIGHT = 320

# Colors (Pyxel 16-color palette)
C_BLACK = 0
C_NAVY = 1
C_PURPLE = 2
C_DGREEN = 3
C_BROWN = 4
C_DGRAY = 5
C_GRAY = 6
C_WHITE = 7
C_RED = 8
C_ORANGE = 9
C_YELLOW = 10
C_GREEN = 11
C_SKYBLUE = 12
C_LAVENDER = 13
C_PINK = 14
C_PEACH = 15

# Font paths (relative to project root)
FONT_MAIN = "assets/umplus_j12r.bdf"
FONT_SMALL = "assets/umplus_j10r.bdf"

# Reputation ranks
REP_RANKS = ["E", "D", "C", "B", "A", "S"]

# Starter agent definitions
STARTERS = [
    {
        "id": "poem",
        "name": "ポエム",
        "type_label": "クリエイター適性",
        "desc": "感性が暴走する\nアーティスト気質",
        "color": C_PINK,
        "stats": {"創造": 8, "技術": 2, "営業": 3, "正確": 2, "体力": 5},
    },
    {
        "id": "bugmaru",
        "name": "バグ丸",
        "type_label": "テック適性",
        "desc": "真面目だけど\n詰めが甘い技術屋",
        "color": C_SKYBLUE,
        "stats": {"創造": 2, "技術": 8, "営業": 2, "正確": 3, "体力": 5},
    },
    {
        "id": "hattari",
        "name": "ハッタリ",
        "type_label": "ビジネス適性",
        "desc": "口が上手い\n営業の天才",
        "color": C_YELLOW,
        "stats": {"創造": 3, "技術": 2, "営業": 8, "正確": 2, "体力": 5},
    },
]

# Random name pool
RANDOM_NAMES = [
    "ギガ太郎", "メガバイ斗", "テラ吉", "ナノ助", "ビット丸",
    "コア次郎", "ラム蔵", "キャッシュ殿", "ログ之介", "バグ美",
    "ポエ美", "アート丸", "クリエ太", "デザ吉", "カラー姫",
    "ドット助", "ピクセル丸", "インク蔵", "パレ太", "キャンバ斗",
    "セール太郎", "マネー丸", "コイン助", "リード吉", "ケーピ太",
    "ディール蔵", "ピッチ之介", "クロージ丸", "ノルマ姫", "プロフィ斗",
    "ぽんこつ丸", "やらかし太郎", "なんとか助", "ゴリ押し蔵",
    "ずんだ丸", "もちもち助", "ふわふわ太", "ガチャ吉", "テキトー之介",
    "エラー太郎", "デバッグ丸", "スタック助", "ヌルポ之介", "セグフォ吉",
    "チャット丸", "プロンプ太", "トークン助", "ハルシ之介", "ファイン丸",
]
