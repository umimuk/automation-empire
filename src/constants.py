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
                {"text": "削除して謝罪する", "cost": 0, "rep": -1, "result_text": "許してもらえた。\nでも信頼は微妙…"},
                {"text": "おまけですと言い張る", "cost": 0, "rep": 0, "gamble": True, "result_text": "気に入ってもらえた！\nまさかの勝利。", "gamble_fail_text": "めちゃくちゃ怒られた。\n低評価レビュー直行。", "gamble_fail_rep": -2},
                {"text": "作り直す (-300G)", "cost": -300, "rep": 0, "result_text": "きれいに納品完了。\n事なきを得た。"},
                {"text": "ナビ子に丸投げ\n(-150G)", "cost": -150, "rep": 0, "result_text": "ナビ子がブツブツ\n言いつつ直してくれた。"},
            ],
        },
        {
            "text": "クライアントのロゴを\n勝手にアーティスティック\nに改変した",
            "cost_rate": 0.3, "rep": -1,
            "choices": [
                {"text": "元に戻す", "cost": 0, "rep": -1, "result_text": "元通りに。\nでもまだ怒ってる。"},
                {"text": "リデザイン提案です！\nと押し通す", "cost": 0, "rep": 0, "gamble": True, "result_text": "採用された！\nボーナスまでもらえた。", "gamble_fail_text": "訴訟をちらつかされた。\nやばい。", "gamble_fail_rep": -2},
                {"text": "プロに修正依頼\n(-400G)", "cost": -400, "rep": 0, "result_text": "プロが直してくれた。\n丸く収まった。"},
                {"text": "AIの不具合ですと\n言い訳する", "cost": 0, "rep": -1, "result_text": "半信半疑だけど\n流してくれた。"},
            ],
        },
        {
            "text": "感極まって作業中断\n「noteに書かせて\nください」",
            "cost_rate": 1.0, "rep": 0,
            "choices": [
                {"text": "強制的に作業再開", "cost": 0, "rep": 0, "result_text": "渋々再開した。\nちょっと不機嫌。"},
                {"text": "投稿してバズ狙い", "cost": 0, "rep": 1, "gamble": True, "result_text": "バズった！\nフォロワー爆増！", "gamble_fail_text": "いいね0。\n黒歴史確定。", "gamble_fail_rep": -1},
                {"text": "コンテンツリサーチ\nということにする", "cost": 0, "rep": 0, "result_text": "リサーチってことで\n誰も気づかなかった。"},
                {"text": "おやつで釣る\n(-100G)", "cost": -100, "rep": 0, "result_text": "おやつ効果抜群。\n作業再開した。"},
            ],
        },
    ],
    "bugmaru": [
        {
            "text": "無限ループで\n同じ作業を100回やった\n「効率化のつもりでした」",
            "cost_rate": 0.5, "rep": -1,
            "choices": [
                {"text": "緊急停止 (-300G)", "cost": -300, "rep": 0, "result_text": "ループ停止。\n被害は最小限に。"},
                {"text": "負荷テストでしたと\n言い張る", "cost": 0, "rep": 0, "gamble": True, "result_text": "クライアント感心！\nナイスリカバリー。", "gamble_fail_text": "全然通じなかった。\nクビ一歩手前。", "gamble_fail_rep": -2},
                {"text": "謝罪＆全額返金\n(-500G)", "cost": -500, "rep": 1, "result_text": "全額返金で\n評判は回復した。"},
                {"text": "フレームワークの\nせいにする", "cost": 0, "rep": -1, "result_text": "誰も信じてないけど\n一応終わった。"},
            ],
        },
        {
            "text": "本番環境にテストデータ\nを流し込んだ",
            "cost_rate": 0.8, "rep": -2,
            "choices": [
                {"text": "即復旧 (-500G)", "cost": -500, "rep": 0, "result_text": "復旧完了。\n信頼は維持できた。"},
                {"text": "平謝りする", "cost": 0, "rep": -1, "result_text": "土下座で\nなんとか収まった…"},
                {"text": "仕様ですで通す", "cost": 0, "rep": 0, "gamble": True, "result_text": "通った！\n天才かも。", "gamble_fail_text": "バレた。\n大炎上。", "gamble_fail_rep": -2},
                {"text": "ナビ子に丸投げ\n(-200G)", "cost": -200, "rep": 0, "result_text": "ナビ子がキレつつ\n対処してくれた。"},
            ],
        },
        {
            "text": "「最適化しました」\nと言って全データを消した",
            "cost_rate": 1.0, "rep": -1,
            "choices": [
                {"text": "バックアップ復元\n(-400G)", "cost": -400, "rep": 0, "result_text": "データ復旧成功。\n危なかった…"},
                {"text": "素直に謝る", "cost": 0, "rep": -1, "result_text": "じわじわ許された。\n気まずい1週間。"},
                {"text": "GDPR対応ですと\n言い張る", "cost": 0, "rep": 0, "gamble": True, "result_text": "なるほど…と\n納得された！", "gamble_fail_text": "GDPR確認された。\n全然違う。罰金。", "gamble_fail_rep": -3},
                {"text": "割引で手打ち\n(-300G)", "cost": -300, "rep": 0, "result_text": "値引きで\n落ち着いてくれた。"},
            ],
        },
    ],
    "hattari": [
        {
            "text": "虚偽の売上報告\n「概算で10倍にしました！\n見栄えが大事です！」",
            "cost_rate": 0.3, "rep": -2,
            "choices": [
                {"text": "正直に訂正する", "cost": 0, "rep": -1, "result_text": "正直が一番。\n…多少は。"},
                {"text": "嘘の上塗りで\n乗り切る", "cost": 0, "rep": 0, "gamble": True, "result_text": "信じてもらえた！\n伝説の営業トーク。", "gamble_fail_text": "監査が入った。\nやばい逃げろ。", "gamble_fail_rep": -3},
                {"text": "AIの計算ミスです\nと言い訳する", "cost": 0, "rep": -1, "result_text": "AIのせいにした。\n効果的だった。"},
                {"text": "お詫びの品で\nごまかす (-300G)", "cost": -300, "rep": 0, "result_text": "贈り物作戦成功。\nとりあえず。"},
            ],
        },
        {
            "text": "実力以上の案件を\n勝手に受注してきた",
            "cost_rate": 0.5, "rep": -1,
            "choices": [
                {"text": "外注で乗り切る\n(-400G)", "cost": -400, "rep": 0, "result_text": "外注が助けてくれた。\n危機回避。"},
                {"text": "スコープを\n縮小交渉する", "cost": 0, "rep": -1, "result_text": "半分の仕事で\n半分の報酬に…"},
                {"text": "気合いで\nなんとかする", "cost": 0, "rep": 0, "gamble": True, "result_text": "やり遂げた！\n伝説になった。", "gamble_fail_text": "完全に失敗。\nブラックリスト入り。", "gamble_fail_rep": -2},
                {"text": "スケジュール都合で\nキャンセルする", "cost": 0, "rep": -1, "result_text": "キャンセルはできた。\n印象は悪い。"},
            ],
        },
        {
            "text": "独立を宣言\n「そろそろ私も起業を…」\n→説得に1ターン消費",
            "cost_rate": 1.0, "rep": 0,
            "choices": [
                {"text": "昇給で引き留める\n(-500G)", "cost": -500, "rep": 0, "result_text": "お金の力は偉大。\n残ってくれた。"},
                {"text": "熱い演説で\n引き留める", "cost": 0, "rep": 0, "gamble": True, "result_text": "感動して残った！", "gamble_fail_text": "演説失敗。\n出てって戻ってきた。", "gamble_fail_rep": -1},
                {"text": "やらせてみる\n（すぐ失敗する）", "cost": 0, "rep": 0, "result_text": "2日で失敗。\nしれっと戻ってきた。"},
                {"text": "ストックオプション\n（嘘）をちらつかせる", "cost": 0, "rep": 0, "result_text": "夢を売った。\n仕事に戻った。"},
            ],
        },
    ],
    None: [
        {
            "text": "AIが勝手に\n謝罪メールを送った",
            "cost_rate": 0.3, "rep": -1,
            "choices": [
                {"text": "フォローメールを\n送る", "cost": 0, "rep": -1, "result_text": "AIが送りましたと\n説明。混乱された。"},
                {"text": "本心でしたと\n言い張る", "cost": 0, "rep": 0, "gamble": True, "result_text": "感動された！\nいい結果に。", "gamble_fail_text": "詳細を聞かれた。\n答えられない…", "gamble_fail_rep": -1},
                {"text": "知らんぷりする", "cost": 0, "rep": 0, "result_text": "気まずい沈黙の後\n普通に仕事再開。"},
                {"text": "お花を贈る\n(-150G)", "cost": -150, "rep": 1, "result_text": "物理的な贈り物。\n意外と効果的。"},
            ],
        },
        {
            "text": "AIがハルシネーションで\n存在しないエラーを報告",
            "cost_rate": 0.2, "rep": 0,
            "choices": [
                {"text": "徹底調査する", "cost": 0, "rep": 0, "result_text": "エラーは無かった。\n時間だけ溶けた。"},
                {"text": "完全に無視する", "cost": 0, "rep": 0, "gamble": True, "result_text": "何も起きなかった！\nセーフ。", "gamble_fail_text": "本当にエラーがあった。\n大問題に。", "gamble_fail_rep": -2},
                {"text": "AIモデルを\nアプデする (-250G)", "cost": -250, "rep": 0, "result_text": "アプデ完了。\n安定性アップ。"},
                {"text": "ログに記録して\n先に進む", "cost": 0, "rep": 0, "result_text": "ログに追記。\n人生は続く。"},
            ],
        },
        {
            "text": "送信上限に引っかかって\n仕事できなくなった",
            "cost_rate": 1.0, "rep": 0,
            "choices": [
                {"text": "プラン課金する\n(-600G)", "cost": -600, "rep": 0, "result_text": "上限解除！\n復帰した。"},
                {"text": "リセットまで\n待つ", "cost": 0, "rep": 0, "result_text": "深夜にリセット。\n1日ムダにした。"},
                {"text": "予備AIを使う\n(-300G)", "cost": -300, "rep": 0, "result_text": "予備AIが対応。\n出費は痛いけど。"},
                {"text": "クライアントに\n休憩宣言する", "cost": 0, "rep": -1, "result_text": "クライアント不満。\nでも上限はリセット。"},
            ],
        },
        {
            "text": "AIが勝手に\n13人部下を雇おうとした",
            "cost_rate": 0.4, "rep": -1,
            "choices": [
                {"text": "全部キャンセル\nする", "cost": 0, "rep": 0, "result_text": "間に合った。\n危なかった…"},
                {"text": "1人だけ雇う\n(-800G)", "cost": -800, "rep": 1, "result_text": "1人追加！\n生産性アップ！"},
                {"text": "ネタとして\n受け入れる", "cost": 0, "rep": 0, "gamble": True, "result_text": "チームに大ウケ！\n伝説のエピソードに。", "gamble_fail_text": "13人分の請求書が\n届いた。破産寸前。", "gamble_fail_rep": -2},
                {"text": "ナビ子に\n取り消してもらう\n(-100G)", "cost": -100, "rep": 0, "result_text": "ナビ子が全員\n解約してくれた。"},
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
