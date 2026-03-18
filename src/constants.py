"""Game constants and data definitions."""
import os

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

# Font paths (absolute, resolved from project root)
FONT_MAIN = os.path.join(_BASE_DIR, "assets", "umplus_j12r.bdf")
FONT_SMALL = os.path.join(_BASE_DIR, "assets", "umplus_j10r.bdf")

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

# ── Job definitions ──
# Each job: (name, base_pay, difficulty_stars, required_stat, stat_threshold, unlock_rank)
JOBS_LV1 = [
    {"name": "データ入力", "pay": 120, "diff": "★", "stat": None, "threshold": 0, "rank": 0},
    {"name": "アンケート代筆", "pay": 150, "diff": "★", "stat": "正確", "threshold": 2, "rank": 0},
    {"name": "リサーチ代行", "pay": 180, "diff": "★☆", "stat": None, "threshold": 0, "rank": 0},
]
JOBS_LV2_CREATOR = [
    {"name": "ブログ記事執筆", "pay": 350, "diff": "★★", "stat": "創造", "threshold": 4, "rank": 1},
    {"name": "AI画像生成・販売", "pay": 500, "diff": "★★", "stat": "創造", "threshold": 5, "rank": 1},
    {"name": "ショート動画制作", "pay": 600, "diff": "★★☆", "stat": "創造", "threshold": 6, "rank": 2},
]
JOBS_LV2_TECH = [
    {"name": "Webサイト制作", "pay": 450, "diff": "★★", "stat": "技術", "threshold": 4, "rank": 1},
    {"name": "Chrome拡張開発", "pay": 400, "diff": "★★", "stat": "技術", "threshold": 5, "rank": 1},
    {"name": "Bot開発", "pay": 550, "diff": "★★☆", "stat": "技術", "threshold": 6, "rank": 2},
]
JOBS_LV2_BIZ = [
    {"name": "アフィリエイト運営", "pay": 300, "diff": "★★", "stat": "営業", "threshold": 4, "rank": 1},
    {"name": "SNS運用代行", "pay": 400, "diff": "★★", "stat": "営業", "threshold": 5, "rank": 1},
    {"name": "プロンプト販売", "pay": 350, "diff": "★★☆", "stat": "営業", "threshold": 6, "rank": 2},
]

ALL_JOBS = JOBS_LV1 + JOBS_LV2_CREATOR + JOBS_LV2_TECH + JOBS_LV2_BIZ

# ── Equipment definitions ──
# effect: "bonus" = % revenue up for stat, "fatigue_reduce" = fatigue per turn reduced,
#         "mishap_reduce" = mishap rate reduced, "all_bonus" = universal % up
EQUIPMENTS = [
    {"name": "GPU増設", "cost": 2000, "effect": "bonus", "stat": "技術", "bonus": 15, "desc": "技術系の収益+15%"},
    {"name": "メモリ拡張", "cost": 2500, "effect": "fatigue_reduce", "stat": None, "bonus": 0, "desc": "負荷の蓄積を軽減"},
    {"name": "高速回線", "cost": 3000, "effect": "bonus", "stat": "創造", "bonus": 15, "desc": "創造系の収益+15%"},
    {"name": "冷却システム", "cost": 3500, "effect": "mishap_reduce", "stat": None, "bonus": 0, "desc": "やらかし率ダウン"},
    {"name": "専用サーバー", "cost": 12000, "effect": "all_bonus", "stat": None, "bonus": 25, "desc": "全副業の収益+25%"},
]

# ── Mishap (やらかし) definitions ──
# agent_id -> list of mishaps; None key = common mishaps
MISHAPS = {
    "poem": [
        {
            "text": "納品物にポエムを混入\n「感動して3行詩を\n添えました」",
            "cost_rate": 0.5, "rep": -1,
            "choices": [
                {"text": "Remove it &\napologize", "cost": 0, "rep": -1, "result_text": "Client forgave you.\nBut trust is shaky."},
                {"text": "Say it was\na bonus gift", "cost": 0, "rep": 0, "gamble": True, "result_text": "They loved it!\nUnexpected win.", "gamble_fail_text": "They hated it.\nBad review.", "gamble_fail_rep": -2},
                {"text": "Redo the work\n(-300G)", "cost": -300, "rep": 0, "result_text": "Clean delivery.\nCrisis averted."},
                {"text": "Ask Naviko\nto handle it", "cost": -150, "rep": 0, "result_text": "Naviko grumbled\nbut fixed it."},
            ],
        },
        {
            "text": "クライアントのロゴを\n勝手にアーティスティック\nに改変した",
            "cost_rate": 0.3, "rep": -1,
            "choices": [
                {"text": "Restore original\nlogo", "cost": 0, "rep": -1, "result_text": "Restored. Client\nstill annoyed."},
                {"text": "Pitch as a\nredesign", "cost": 0, "rep": 0, "gamble": True, "result_text": "They bought it!\nBonus incoming.", "gamble_fail_text": "Lawsuit threat.\nAbort abort.", "gamble_fail_rep": -2},
                {"text": "Hire a pro\nto fix (-400G)", "cost": -400, "rep": 0, "result_text": "Pro fixed it.\nNo harm done."},
                {"text": "Blame an\nAI glitch", "cost": 0, "rep": -1, "result_text": "Half-believed.\nMoved on."},
            ],
        },
        {
            "text": "感極まって作業中断\n「noteに書かせて\nください」",
            "cost_rate": 1.0, "rep": 0,
            "choices": [
                {"text": "Force resume\nwork", "cost": 0, "rep": 0, "result_text": "Back on track.\nA bit grumpy."},
                {"text": "Post it &\ngain fans", "cost": 0, "rep": 1, "gamble": True, "result_text": "Went viral!\nNew followers!", "gamble_fail_text": "Zero likes.\nSo cringe.", "gamble_fail_rep": -1},
                {"text": "Call it content\nresearch", "cost": 0, "rep": 0, "result_text": "Called it research.\nNo one noticed."},
                {"text": "Bribe with\nsnacks (-100G)", "cost": -100, "rep": 0, "result_text": "Snacks worked.\nWork resumed."},
            ],
        },
    ],
    "bugmaru": [
        {
            "text": "無限ループで\n同じ作業を100回やった\n「効率化のつもりでした」",
            "cost_rate": 0.5, "rep": -1,
            "choices": [
                {"text": "Emergency stop\n(-300G)", "cost": -300, "rep": 0, "result_text": "Loop stopped.\nLoss contained."},
                {"text": "Call it\nstress testing", "cost": 0, "rep": 0, "gamble": True, "result_text": "Client impressed!\nNicely played.", "gamble_fail_text": "Not impressed.\nYou're fired.", "gamble_fail_rep": -2},
                {"text": "Apologize &\nrefund (-500G)", "cost": -500, "rep": 1, "result_text": "Full refund.\nRep improved."},
                {"text": "Blame the\nframework", "cost": 0, "rep": -1, "result_text": "Nobody believed you.\nBut it ended."},
            ],
        },
        {
            "text": "本番環境にテストデータ\nを流し込んだ",
            "cost_rate": 0.8, "rep": -2,
            "choices": [
                {"text": "Instant fix\n(-500G)", "cost": -500, "rep": 0, "result_text": "Fixed fast.\nTrust maintained."},
                {"text": "Apologize\nhumbly", "cost": 0, "rep": -1, "result_text": "Bowed deeply.\nCalmed down."},
                {"text": "Call it a\nfeature", "cost": 0, "rep": 0, "gamble": True, "result_text": "They believed it!\nGenius!", "gamble_fail_text": "Exposed. Disaster.\nBig drama.", "gamble_fail_rep": -2},
                {"text": "Ask Naviko\n(-200G)", "cost": -200, "rep": 0, "result_text": "Naviko raged\nbut fixed it."},
            ],
        },
        {
            "text": "「最適化しました」\nと言って全データを消した",
            "cost_rate": 1.0, "rep": -1,
            "choices": [
                {"text": "Restore backup\n(-400G)", "cost": -400, "rep": 0, "result_text": "Data restored.\nClose call."},
                {"text": "Grovel and\nadmit mistake", "cost": 0, "rep": -1, "result_text": "Forgiven slowly.\nAwkward week."},
                {"text": "Claim GDPR\ncleanup", "cost": 0, "rep": 0, "gamble": True, "result_text": "They nodded!\nDodged it.", "gamble_fail_text": "They checked GDPR.\nNope. Big fine.", "gamble_fail_rep": -3},
                {"text": "Offer discount\n(-300G)", "cost": -300, "rep": 0, "result_text": "Discount calmed\nthem down."},
            ],
        },
    ],
    "hattari": [
        {
            "text": "虚偽の売上報告\n「概算で10倍にしました！\n見栄えが大事です！」",
            "cost_rate": 0.3, "rep": -2,
            "choices": [
                {"text": "Come clean\nimmediately", "cost": 0, "rep": -1, "result_text": "Honesty helped.\nSlightly."},
                {"text": "Double down\non the lie", "cost": 0, "rep": 0, "gamble": True, "result_text": "They believed it!\nLegend.", "gamble_fail_text": "Audit requested.\nRun!", "gamble_fail_rep": -3},
                {"text": "Blame AI\nfor the error", "cost": 0, "rep": -1, "result_text": "AI took the blame.\nEffective."},
                {"text": "Distract with\ngifts (-300G)", "cost": -300, "rep": 0, "result_text": "Gifts distracted.\nFor now."},
            ],
        },
        {
            "text": "実力以上の案件を\n勝手に受注してきた",
            "cost_rate": 0.5, "rep": -1,
            "choices": [
                {"text": "Hire temp help\n(-400G)", "cost": -400, "rep": 0, "result_text": "Temp handled it.\nBullet dodged."},
                {"text": "Negotiate\nscope down", "cost": 0, "rep": -1, "result_text": "Half job done.\nHalf price."},
                {"text": "Wing it\nfully", "cost": 0, "rep": 0, "gamble": True, "result_text": "Nailed it!\nLegendary.", "gamble_fail_text": "Total failure.\nBlacklisted.", "gamble_fail_rep": -2},
                {"text": "Blame a\nschedule conflict", "cost": 0, "rep": -1, "result_text": "Cancelled cleanly.\nNot great."},
            ],
        },
        {
            "text": "独立を宣言\n「そろそろ私も起業を…」\n→説得に1ターン消費",
            "cost_rate": 1.0, "rep": 0,
            "choices": [
                {"text": "Give a raise\n(-500G)", "cost": -500, "rep": 0, "result_text": "Money talked.\nStayed put."},
                {"text": "Motivational\nspeech", "cost": 0, "rep": 0, "gamble": True, "result_text": "Inspired! Stayed.", "gamble_fail_text": "Speech failed.\nLeft then returned.", "gamble_fail_rep": -1},
                {"text": "Let them try\nand fail", "cost": 0, "rep": 0, "result_text": "Failed in 2 days.\nReturned sheepish."},
                {"text": "Promise equity\n(fake)", "cost": 0, "rep": 0, "result_text": "Dream sold.\nBack to work."},
            ],
        },
    ],
    None: [
        {
            "text": "AIが勝手に\n謝罪メールを送った",
            "cost_rate": 0.3, "rep": -1,
            "choices": [
                {"text": "Send a\nfollow-up", "cost": 0, "rep": -1, "result_text": "Explained the AI.\nThey were confused."},
                {"text": "Own it as\ngenuine", "cost": 0, "rep": 0, "gamble": True, "result_text": "They were touched!\nGood outcome.", "gamble_fail_text": "They wanted details.\nCould not provide.", "gamble_fail_rep": -1},
                {"text": "Pretend it\nnever happened", "cost": 0, "rep": 0, "result_text": "Awkward silence.\nThen business resumed."},
                {"text": "Send flowers\n(-150G)", "cost": -150, "rep": 1, "result_text": "Physical gift.\nSurprisingly effective."},
            ],
        },
        {
            "text": "AIがハルシネーションで\n存在しないエラーを報告",
            "cost_rate": 0.2, "rep": 0,
            "choices": [
                {"text": "Investigate\nthoroughly", "cost": 0, "rep": 0, "result_text": "No error found.\nWasted time."},
                {"text": "Ignore it\ncompletely", "cost": 0, "rep": 0, "gamble": True, "result_text": "Nothing happened!\nPhew.", "gamble_fail_text": "Real error existed.\nBig problem.", "gamble_fail_rep": -2},
                {"text": "Upgrade AI\nmodel (-250G)", "cost": -250, "rep": 0, "result_text": "Upgraded. More\nstable now."},
                {"text": "Log it and\nmove on", "cost": 0, "rep": 0, "result_text": "Added to log.\nLife goes on."},
            ],
        },
        {
            "text": "送信上限に引っかかって\n仕事できなくなった",
            "cost_rate": 1.0, "rep": 0,
            "choices": [
                {"text": "Upgrade plan\n(-600G)", "cost": -600, "rep": 0, "result_text": "Limits raised.\nBack online."},
                {"text": "Wait it out", "cost": 0, "rep": 0, "result_text": "Reset by midnight.\nLost a day."},
                {"text": "Use backup AI\n(-300G)", "cost": -300, "rep": 0, "result_text": "Backup handled it.\nExpensive but fine."},
                {"text": "Tell client\nneed a break", "cost": 0, "rep": -1, "result_text": "Client unhappy.\nBut limits reset."},
            ],
        },
        {
            "text": "AIが勝手に\n13人部下を雇おうとした",
            "cost_rate": 0.4, "rep": -1,
            "choices": [
                {"text": "Cancel all\nhire requests", "cost": 0, "rep": 0, "result_text": "Cancelled in time.\nClose call."},
                {"text": "Hire just one\n(-800G)", "cost": -800, "rep": 1, "result_text": "One new hire.\nProductivity up!"},
                {"text": "Let it ride\nfor laughs", "cost": 0, "rep": 0, "gamble": True, "result_text": "Team loved story!\nLegend status.", "gamble_fail_text": "13 invoices arrived.\nNearly bankrupt.", "gamble_fail_rep": -2},
                {"text": "Ask Naviko\nto undo it", "cost": -100, "rep": 0, "result_text": "Naviko unsubscribed\nthem all."},
            ],
        },
    ],
}

# Naviko comments for mishaps
NAVIKO_MISHAP = [
    "…は？", "いや何やってんの", "聞いてない聞いてない",
    "まあ、想定の範囲内…\nじゃないわ", "またか…",
]

# Naviko comments for success
NAVIKO_SUCCESS = [
    "順調だね。", "まあまあかな。", "この調子！",
    "悪くないよ。", "頑張ってるね。",
    "やるじゃん。", "いい感じ。",
]

# Naviko idle (no job selected) comments - directed at player
NAVIKO_IDLE = [
    "…ボス、今週\n何もしてないけど？",
    "指示くれないと\nAI暇なんだけど。",
    "案件選んでよ。\nAI、やることないんだけど。",
    "ボスがサボると\n全員ヒマになるんだよ？",
]

# Naviko overload warnings
NAVIKO_OVERLOAD = [
    "負荷高いよ。\nこのままだとやらかすよ？",
    "負荷やばくない？\nデフラグした方がいいよ。",
    "⚠ 負荷限界近い。\nやらかし率上がってるよ。",
]

# Naviko defrag comments
NAVIKO_DEFRAG = [
    "デフラグ完了！\nスッキリしたね。",
    "負荷リセット。\nまたバリバリ働けるよ。",
    "最適化完了。\n次のターンから全力で。",
]

# AI weakness: agent_id -> list of weak stat names (for mishap rate calc)
AI_WEAKNESS = {
    "poem": ["技術", "正確"],
    "bugmaru": ["営業", "創造"],
    "hattari": ["技術", "正確"],
}

# AI strengths: agent_id -> strong stat
AI_STRENGTH = {
    "poem": "創造",
    "bugmaru": "技術",
    "hattari": "営業",
}

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
