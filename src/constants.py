"""Game constants and data definitions."""
import os

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Screen (9:16 aspect ratio for smartphone)
WIDTH = 270
HEIGHT = 480

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
        "stats": {"創造": 3, "技術": 1, "営業": 1, "正確": 1, "体力": 2},
    },
    {
        "id": "bugmaru",
        "name": "バグ丸",
        "type_label": "テック適性",
        "desc": "真面目だけど\n詰めが甘い技術屋",
        "color": C_SKYBLUE,
        "stats": {"創造": 1, "技術": 3, "営業": 1, "正確": 2, "体力": 1},
    },
    {
        "id": "hattari",
        "name": "ハッタリ",
        "type_label": "ビジネス適性",
        "desc": "口が上手い\n営業の天才",
        "color": C_YELLOW,
        "stats": {"創造": 1, "技術": 1, "営業": 3, "正確": 1, "体力": 2},
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

# ── Phase 5: Higher-tier Jobs ──
JOBS_LV3_CREATOR = [
    {"name": "YouTube動画制作", "pay": 900, "diff": "★★★", "stat": "創造", "threshold": 7, "rank": 2},
    {"name": "電子書籍出版", "pay": 800, "diff": "★★★", "stat": "創造", "threshold": 6, "rank": 2},
]
JOBS_LV3_TECH = [
    {"name": "ブラウザゲーム開発", "pay": 1000, "diff": "★★★", "stat": "技術", "threshold": 7, "rank": 2},
    {"name": "アプリ開発", "pay": 950, "diff": "★★★", "stat": "技術", "threshold": 6, "rank": 2},
]
JOBS_LV3_BIZ = [
    {"name": "note有料記事", "pay": 750, "diff": "★★★", "stat": "営業", "threshold": 6, "rank": 2},
    {"name": "占い・診断サービス", "pay": 700, "diff": "★★★", "stat": "営業", "threshold": 7, "rank": 3},
]
JOBS_LV4 = [
    {"name": "ツール開発・SaaS", "pay": 1500, "diff": "★★★★", "stat": "技術", "threshold": 8, "rank": 3},
    {"name": "オンライン講座", "pay": 1300, "diff": "★★★★", "stat": "営業", "threshold": 8, "rank": 3},
]
JOBS_LV5 = [
    {"name": "AI組織運営", "pay": 2500, "diff": "★★★★★", "stat": None, "threshold": 0, "rank": 4},
]

ALL_JOBS = (JOBS_LV1 + JOBS_LV2_CREATOR + JOBS_LV2_TECH + JOBS_LV2_BIZ
            + JOBS_LV3_CREATOR + JOBS_LV3_TECH + JOBS_LV3_BIZ
            + JOBS_LV4 + JOBS_LV5)

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
                {"text": "丁寧に謝罪する", "cost": 0, "rep": -1, "result_text": "許してもらえた。\nでも信頼は微妙…"},
                {"text": "アートですと\n言い張る", "gamble": True, "cost": 200, "rep": 1, "result_text": "気に入ってもらえた！\nボーナスまで出た。", "gamble_fail_text": "めちゃくちゃ怒られた。\n低評価レビュー直行。", "gamble_fail_rep": -2, "gamble_fail_cost": 0},
                {"text": "作り直す", "cost": -300, "rep": 0, "result_text": "きれいに納品完了。\n事なきを得た。"},
                {"text": "AIモデルを\n再調整する", "cost": -200, "rep": 0, "fatigue": -2, "result_text": "再調整完了。\n動作も安定した。"},
            ],
        },
        {
            "text": "クライアントのロゴを\n勝手にアーティスティック\nに改変した",
            "cost_rate": 0.3, "rep": -1,
            "choices": [
                {"text": "元に戻す", "cost": 0, "rep": -1, "result_text": "元通りに。\nでもまだ怒ってる。"},
                {"text": "リデザイン提案です！\nと押し通す", "gamble": True, "cost": 500, "rep": 1, "result_text": "採用された！\nボーナスまでもらえた。", "gamble_fail_text": "訴訟をちらつかされた。\nやばい。", "gamble_fail_rep": -2, "gamble_fail_cost": -200},
                {"text": "プロに修正依頼する", "cost": -400, "rep": 0, "result_text": "プロが直してくれた。\n丸く収まった。"},
                {"text": "自主学習と説明して\n改善を約束", "cost": 0, "rep": 0, "fatigue": -1, "result_text": "学習の成果ってことで\n落ち着いた。負荷も改善。"},
            ],
        },
        {
            "text": "感極まって作業中断\n「noteに書かせて\nください」",
            "cost_rate": 1.0, "rep": 0,
            "choices": [
                {"text": "強制的に作業再開", "cost": 0, "rep": 0, "fatigue": 1, "result_text": "渋々再開した。\nちょっと不機嫌。負荷↑"},
                {"text": "投稿してバズ狙い", "gamble": True, "cost": 300, "rep": 1, "result_text": "バズった！\nフォロワー爆増！", "gamble_fail_text": "いいね0。\n黒歴史確定。", "gamble_fail_rep": -1, "gamble_fail_cost": 0},
                {"text": "リサーチということに\nする", "cost": 0, "rep": 0, "result_text": "リサーチってことで\n誰も気づかなかった。"},
                {"text": "キャッシュを\nクリアする", "cost": -100, "rep": 0, "fatigue": -1, "result_text": "キャッシュ削除完了。\n動作も気分もスッキリ！"},
            ],
        },
    ],
    "bugmaru": [
        {
            "text": "無限ループで\n同じ作業を100回やった\n「効率化のつもりでした」",
            "cost_rate": 0.5, "rep": -1,
            "choices": [
                {"text": "緊急停止して復旧", "cost": -200, "rep": 0, "result_text": "ループ停止。\n被害は最小限に。"},
                {"text": "負荷テストでしたと\n言い張る", "gamble": True, "cost": 300, "rep": 1, "result_text": "クライアント感心！\nナイスリカバリー。", "gamble_fail_text": "全然通じなかった。\nクビ一歩手前。", "gamble_fail_rep": -2, "gamble_fail_cost": 0},
                {"text": "全額返金で\n信頼を回復する", "cost": -500, "rep": 1, "result_text": "全額返金で\n評判は回復した。"},
                {"text": "メモリ増設して\n根本対策する", "cost": -300, "rep": 0, "fatigue": -3, "result_text": "メモリ増設完了。\n負荷も大幅ダウン！"},
            ],
        },
        {
            "text": "本番環境にテストデータ\nを流し込んだ",
            "cost_rate": 0.8, "rep": -2,
            "choices": [
                {"text": "即座に復旧する", "cost": -400, "rep": 0, "result_text": "復旧完了。\n信頼は維持できた。"},
                {"text": "平謝りする", "cost": 0, "rep": -1, "result_text": "土下座で\nなんとか収まった…"},
                {"text": "仕様ですで通す", "gamble": True, "cost": 0, "rep": 1, "result_text": "通った！\n天才かも。", "gamble_fail_text": "バレた。大炎上。\n賠償金まで請求された。", "gamble_fail_rep": -2, "gamble_fail_cost": -300},
                {"text": "AIプランを\nアップグレード", "cost": -500, "rep": 0, "fatigue": -3, "result_text": "プランアップグレード！\n復旧も安定性もバッチリ。"},
            ],
        },
        {
            "text": "「最適化しました」\nと言って全データを消した",
            "cost_rate": 1.0, "rep": -1,
            "choices": [
                {"text": "バックアップから復元", "cost": -300, "rep": 0, "result_text": "データ復旧成功。\n危なかった…"},
                {"text": "素直に謝る", "cost": 0, "rep": -1, "result_text": "じわじわ許された。\n気まずい1週間。"},
                {"text": "GDPR対応ですと\n言い張る", "gamble": True, "cost": 200, "rep": 1, "result_text": "なるほど…と\n納得された！感謝まで。", "gamble_fail_text": "GDPR確認された。\n全然違う。罰金。", "gamble_fail_rep": -3, "gamble_fail_cost": -400},
                {"text": "AIモデルを\nアップデートする", "cost": -350, "rep": 0, "fatigue": -2, "result_text": "アプデ完了。\n再発防止＆負荷軽減。"},
            ],
        },
    ],
    "hattari": [
        {
            "text": "虚偽の売上報告\n「概算で10倍にしました！\n見栄えが大事です！」",
            "cost_rate": 0.3, "rep": -2,
            "choices": [
                {"text": "正直に訂正する", "cost": 0, "rep": -1, "result_text": "正直が一番。\n…多少は。"},
                {"text": "嘘の上塗りで\n乗り切る", "gamble": True, "cost": 500, "rep": 0, "result_text": "信じてもらえた！\n伝説の営業トーク。", "gamble_fail_text": "監査が入った。\nやばい。賠償金。", "gamble_fail_rep": -3, "gamble_fail_cost": -300},
                {"text": "AIのせいにする", "cost": 0, "rep": -1, "result_text": "AIのせいにした。\n効果的だった。"},
                {"text": "コンサル費用で示談", "cost": -400, "rep": 0, "result_text": "贈り物作戦成功。\nとりあえず解決。"},
            ],
        },
        {
            "text": "実力以上の案件を\n勝手に受注してきた",
            "cost_rate": 0.5, "rep": -1,
            "choices": [
                {"text": "外注で乗り切る", "cost": -400, "rep": 0, "result_text": "外注が助けてくれた。\n危機回避。"},
                {"text": "スコープを\n縮小交渉する", "cost": 0, "rep": -1, "result_text": "半分の仕事で\n半分の報酬に…"},
                {"text": "気合いで\nなんとかする", "gamble": True, "cost": 600, "rep": 1, "result_text": "やり遂げた！\n伝説になった。報酬も増！", "gamble_fail_text": "完全に失敗。\nブラックリスト入り。", "gamble_fail_rep": -2, "gamble_fail_cost": 0},
                {"text": "AI強化して\n対応力アップ", "cost": -350, "rep": 0, "fatigue": -2, "result_text": "AI強化完了。\n今後はもっと上手くやれる。"},
            ],
        },
        {
            "text": "独立を宣言\n「そろそろ私も起業を…」\n→説得に1ターン消費",
            "cost_rate": 1.0, "rep": 0,
            "choices": [
                {"text": "昇給で引き留める", "cost": -500, "rep": 0, "result_text": "お金の力は偉大。\n残ってくれた。"},
                {"text": "熱い演説で\n引き留める", "gamble": True, "cost": 0, "rep": 1, "fatigue": -1, "result_text": "感動して残った！\nやる気もアップ！", "gamble_fail_text": "演説失敗。\n出てって戻ってきた。", "gamble_fail_rep": -1, "gamble_fail_cost": 0},
                {"text": "やらせてみる", "cost": 0, "rep": 0, "result_text": "2日で失敗。\nしれっと戻ってきた。"},
                {"text": "ストックオプションを\nちらつかせる", "cost": 0, "rep": 0, "fatigue": -1, "result_text": "夢を売った。\nモチベ回復して仕事再開。"},
            ],
        },
    ],
    None: [
        {
            "text": "AIが勝手に\n謝罪メールを送った",
            "cost_rate": 0.3, "rep": -1,
            "choices": [
                {"text": "フォローメールを\n送る", "cost": 0, "rep": -1, "result_text": "AIが送りましたと\n説明。混乱された。"},
                {"text": "本心でしたと\n言い張る", "gamble": True, "cost": 200, "rep": 1, "result_text": "感動された！\n追加案件まで来た！", "gamble_fail_text": "詳細を聞かれた。\n答えられない…", "gamble_fail_rep": -1, "gamble_fail_cost": 0},
                {"text": "知らんぷりする", "cost": 0, "rep": 0, "result_text": "気まずい沈黙の後\n普通に仕事再開。"},
                {"text": "お花を贈って\nフォローする", "cost": -150, "rep": 1, "result_text": "物理的な贈り物。\n意外と効果的。"},
            ],
        },
        {
            "text": "AIがハルシネーションで\n存在しないエラーを報告",
            "cost_rate": 0.2, "rep": 0,
            "choices": [
                {"text": "徹底調査する", "cost": -100, "rep": 0, "result_text": "エラーは無かった。\n時間もお金も溶けた。"},
                {"text": "完全に無視する", "gamble": True, "cost": 0, "rep": 0, "result_text": "何も起きなかった！\nセーフ。", "gamble_fail_text": "本当にエラーがあった。\n大問題に。賠償発生。", "gamble_fail_rep": -2, "gamble_fail_cost": -300},
                {"text": "AIモデルを\nアップデートする", "cost": -250, "rep": 0, "fatigue": -3, "result_text": "アプデ完了。\n安定性も負荷も改善！"},
                {"text": "ログに記録して\n先に進む", "cost": 0, "rep": 0, "result_text": "ログに追記。\n人生は続く。"},
            ],
        },
        {
            "text": "送信上限に引っかかって\n仕事できなくなった",
            "cost_rate": 1.0, "rep": 0,
            "choices": [
                {"text": "プラン課金する", "cost": -500, "rep": 0, "fatigue": -4, "result_text": "上限解除！\n負荷も大幅リセット！"},
                {"text": "リセットまで待つ", "cost": 0, "rep": 0, "fatigue": 1, "result_text": "深夜にリセット。\n1日ムダにした。負荷↑"},
                {"text": "予備AIを起動する", "cost": -300, "rep": 0, "fatigue": -1, "result_text": "予備AIが対応。\n負荷も少し軽減。"},
                {"text": "クライアントに\n休憩宣言する", "cost": 0, "rep": -1, "fatigue": -2, "result_text": "クライアント不満…\nでも負荷はリセットできた。"},
            ],
        },
        {
            "text": "AIが勝手に\n13人部下を雇おうとした",
            "cost_rate": 0.4, "rep": -1,
            "choices": [
                {"text": "全部キャンセルする", "cost": 0, "rep": 0, "result_text": "間に合った。\n危なかった…"},
                {"text": "1人だけ雇って強化", "cost": -800, "rep": 0, "result_text": "雇ったけどメモリ不足で\nフリーズ。使い物にならず…"},
                {"text": "ネタとして\n受け入れる", "gamble": True, "cost": -1300, "rep": 0, "result_text": "13人起動→即メモリ不足。\n全員フリーズして終了。", "gamble_fail_text": "13人分の請求が来た。\nしかも全員フリーズ。最悪。", "gamble_fail_rep": -2, "gamble_fail_cost": -1300},
                {"text": "ナビ子に\n取り消してもらう", "cost": -100, "rep": 0, "result_text": "ナビ子が全員\n解約してくれた。"},
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

# ── Phase 4: Office levels ──
OFFICE_LEVELS = [
    {"name": "自宅の一角", "cost": 0, "bonus": 0, "desc": "すべてはここから"},
    {"name": "ワンルーム", "cost": 5000, "bonus": 10, "desc": "収益+10%"},
    {"name": "フロアオフィス", "cost": 20000, "bonus": 15, "desc": "収益+15% 負荷回復UP"},
    {"name": "ビル1棟", "cost": 100000, "bonus": 25, "desc": "収益+25% 負荷回復UP"},
    {"name": "AI帝国タワー", "cost": 500000, "bonus": 40, "desc": "収益+40% 負荷回復UP"},
]

# ── Phase 4: Tax event ──
TAX_EVENT_CHOICES = [
    {"text": "自分で申告する", "tax_rate": 0.10, "rep": 0, "fatigue": 1,
     "result_text": "正確に申告完了。\n時間はかかったけど安心。"},
    {"text": "AIに任せる", "gamble": True, "tax_rate": 0.05, "rep": 0,
     "result_text": "AIが節税テクを発見！\n還付金ゲット！",
     "gamble_fail_tax_rate": 0.25, "gamble_fail_rep": -1,
     "gamble_fail_text": "AIが経費を水増し…\n税務調査が入った。"},
    {"text": "税理士に依頼する", "tax_rate": 0.15, "rep": 0,
     "result_text": "プロに任せて安心。\nちょっとお高い。"},
    {"text": "放置する", "tax_rate": 0.30, "rep": -2,
     "result_text": "追徴課税キター！\n評判もガタ落ち…"},
]

TAX_AGENT_FAILS = {
    "poem": "申告書にポエムを書いた。\n税務署困惑。",
    "bugmaru": "計算を無限ループ。\n期限切れ…",
    "hattari": "経費を10倍に水増し。\n税務調査確定。",
}

# ── Phase 4: Monthly report ──
# 条件別ナビ子セリフ（優先順位順に判定）
NAVIKO_MONTHLY_REVENUE_UP = [
    "めっちゃ伸びてるじゃん。",
    "この調子この調子。",
]
NAVIKO_MONTHLY_REVENUE_DOWN = [
    "先月より減ってるけど大丈夫？",
    "ちょっと失速気味？",
]
NAVIKO_MONTHLY_MISHAP_MANY = [
    "やらかし多くない？",
    "落ち着いて行こ？",
]
NAVIKO_MONTHLY_MISHAP0 = [
    "平和な月だったね。",
    "やらかしゼロは偉い。",
]
NAVIKO_MONTHLY_RANKUP = [
    "評判上がったじゃん。",
]
NAVIKO_MONTHLY_BROKE = [
    "金欠やばくない？",
    "節約しよ…",
]
NAVIKO_MONTHLY_DEFAULT = [
    "まぁぼちぼちだね。",
    "順調順調。",
]

# ── Phase 4: Rank up ──
NAVIKO_RANKUP = [
    "評判ランクUP！\nいい感じだよ。",
    "ランク昇格！\nいい案件が来るようになるよ。",
    "ランクアップ！\n経営判断が効いてるね。",
]

NAVIKO_TAX = [
    "確定申告の季節だよ。\nどう対応する？",
    "税金の時間。副業の宿命だね。",
    "申告しないと追徴課税だからね？",
]

# ── Phase 5: Synergy Bonuses ──
SYNERGIES = [
    {"jobs": ["ブログ記事執筆", "アフィリエイト運営"], "name": "ブロガー覚醒", "bonus": 30, "desc": "収益+30%"},
    {"jobs": ["AI画像生成・販売", "ショート動画制作"], "name": "ビジュアル爆撃", "bonus": 25, "desc": "収益+25%"},
    {"jobs": ["Bot開発", "SNS運用代行"], "name": "自動化コンボ", "bonus": 30, "desc": "収益+30%"},
    {"jobs": ["ブラウザゲーム開発", "YouTube動画制作"], "name": "実況セルフプロモ", "bonus": 25, "desc": "収益+25%"},
    {"jobs": ["note有料記事", "オンライン講座"], "name": "知識マネタイザー", "bonus": 30, "desc": "収益+30%"},
    {"jobs": ["占い・診断サービス", "プロンプト販売"], "name": "神秘のAI商人", "bonus": 20, "desc": "収益+20%"},
]

# ── Phase 5: Hidden Titles ──
TITLES = [
    {"id": "loose_ceo", "name": "放任主義CEO", "desc": "やらかし10回連続"},
    {"id": "emperor", "name": "自動化帝王", "desc": "全副業を制覇"},
    {"id": "legend", "name": "レジェンド経営者", "desc": "評判Sランクに到達"},
    {"id": "neet", "name": "不労所得マスター", "desc": "10週連続サボって生存"},
    {"id": "careful", "name": "石橋慎重経営", "desc": "やらかしゼロでLv10到達"},
    {"id": "rich", "name": "札束で殴る経営", "desc": "所持金10万G到達"},
    {"id": "perfectionist", "name": "完璧主義者", "desc": "やらかし0回でクリア"},
]

# ── Phase 5: Game length ──
GAME_LENGTH_WEEKS = 144  # 3 years

# ── Phase 5: Ending definitions ──
ENDINGS = [
    {
        "id": "empire",
        "name": "帝国完成",
        "naviko": "やるじゃん、ボス。\n本当に帝国作っちゃったね。\n…私がいたからだけど。",
        "desc": "AI副業事務所は\n「自動化帝国」として\n業界の頂点に立った。",
    },
    {
        "id": "rebellion",
        "name": "AI反乱",
        "naviko": "ついにAIが反乱。\nあなた、逆に経営される\n側になっちゃったよ。",
        "desc": "やらかしが限界を超え\nAIが独立宣言。\n逆に雇われる側に。",
    },
    {
        "id": "stable",
        "name": "中堅事務所",
        "naviko": "まあまあかな。\n安定経営ってやつだね。\nまだまだ伸びしろあるよ。",
        "desc": "安定した副業事務所。\n大きくはないけど\n「まだまだこれから」。",
    },
    {
        "id": "small",
        "name": "零細事務所",
        "naviko": "…ボス、大丈夫？\nAIに逃げられかけたよ。\nでも諦めなかったのは偉い。",
        "desc": "零細副業事務所。\nAIに逃げられかけたけど\nあなたはまだ諦めない。",
    },
    {
        "id": "default",
        "name": "普通エンド",
        "naviko": "3年間お疲れ。\nまあ、悪くなかったよ。\n…たぶん。",
        "desc": "3年間の副業経営が終了。\n経験値はプライスレス。",
    },
]

NAVIKO_SYNERGY = [
    "シナジー発動！\n組み合わせが効いてる！",
    "コンボ発見！\n相乗効果で収益UP！",
]

NAVIKO_TITLE = [
    "おっ、称号獲得！\nやるじゃん。",
    "新しい称号だよ。\nコレクション増えたね。",
]
