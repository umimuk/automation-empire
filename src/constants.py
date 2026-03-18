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
SCENE_ROUTE_SELECT = 7
SCENE_SHOP = 8

# 御三家タイプ
AI_POEM = 0     # ポエム（クリエイター適性）
AI_BUGMARU = 1  # バグ丸（テック適性）
AI_HATTARI = 2  # ハッタリ（ビジネス適性）

AI_NAMES_DEFAULT = ["Poem", "Bugmaru", "Hattari"]
AI_TYPES = ["Creator", "Tech", "Business"]
AI_COLORS = [COL_PINK, COL_BLUE, COL_ORANGE]

# ルート定数
ROUTE_NONE = -1
ROUTE_CREATOR = 0
ROUTE_TECH = 1
ROUTE_BUSINESS = 2
ROUTE_NAMES = ["Creator", "Tech", "Business"]
ROUTE_COLORS = [COL_PINK, COL_BLUE, COL_ORANGE]
ROUTE_ICONS = ["Art", "Code", "Biz"]

# 御三家の適性ルートマッピング
# ai_type -> 適性ルート
AI_APTITUDE = {
    AI_POEM: ROUTE_CREATOR,
    AI_BUGMARU: ROUTE_TECH,
    AI_HATTARI: ROUTE_BUSINESS,
}

# 御三家の苦手ルートマッピング
# ai_type -> 苦手ルート
AI_WEAKNESS = {
    AI_POEM: ROUTE_BUSINESS,
    AI_BUGMARU: ROUTE_BUSINESS,
    AI_HATTARI: ROUTE_CREATOR,
}

# 適性ボーナス/ペナルティ
APTITUDE_BONUS = 1.5       # 適性ルートの成長倍率
APTITUDE_NORMAL = 1.0      # 普通
APTITUDE_PENALTY = 0.7     # 苦手ルートの成長倍率
APTITUDE_INCIDENT_BONUS = 0.5   # 適性ルートのやらかし倍率（低い=少ない）
APTITUDE_INCIDENT_PENALTY = 2.0  # 苦手ルートのやらかし倍率

# ===== 副業データ（全21種） =====

# Lv1: 下積み（共通3種）
JOB_LV1 = [
    {"id": 0, "name": "Data Entry", "base_income": 1,
     "cost": 0, "route": None, "level": 1,
     "desc": "Your first income. Click basics."},
    {"id": 1, "name": "Survey Writing", "base_income": 2,
     "cost": 50, "route": None, "level": 1,
     "desc": "Improves click efficiency."},
    {"id": 2, "name": "Research Asst.", "base_income": 3,
     "cost": 150, "route": None, "level": 1,
     "desc": "Gain info resources."},
]

# Lv2: 3ルート分岐（各3種＝9種）
JOB_LV2 = [
    # クリエイタールート
    {"id": 3, "name": "Blog Writing", "base_income": 5,
     "cost": 500, "route": ROUTE_CREATOR, "level": 2,
     "desc": "Steady page views."},
    {"id": 4, "name": "AI Art Sales", "base_income": 8,
     "cost": 800, "route": ROUTE_CREATOR, "level": 2,
     "desc": "Hit or miss. Big potential."},
    {"id": 5, "name": "Short Videos", "base_income": 10,
     "cost": 1200, "route": ROUTE_CREATOR, "level": 2,
     "desc": "Viral power. Explosive."},
    # テックルート
    {"id": 6, "name": "Web Dev", "base_income": 7,
     "cost": 600, "route": ROUTE_TECH, "level": 2,
     "desc": "High unit price."},
    {"id": 7, "name": "Chrome Ext.", "base_income": 6,
     "cost": 700, "route": ROUTE_TECH, "level": 2,
     "desc": "Niche but stable."},
    {"id": 8, "name": "Bot Dev", "base_income": 9,
     "cost": 1000, "route": ROUTE_TECH, "level": 2,
     "desc": "Subscription income."},
    # ビジネスルート
    {"id": 9, "name": "Affiliate", "base_income": 6,
     "cost": 500, "route": ROUTE_BUSINESS, "level": 2,
     "desc": "Passive income basics."},
    {"id": 10, "name": "SNS Management", "base_income": 8,
     "cost": 800, "route": ROUTE_BUSINESS, "level": 2,
     "desc": "Client work."},
    {"id": 11, "name": "Prompt Sales", "base_income": 12,
     "cost": 1100, "route": ROUTE_BUSINESS, "level": 2,
     "desc": "Zero cost. Instant cash."},
]

# Lv3: ルート深化（各2種＝6種）
JOB_LV3 = [
    # クリエイター上級
    {"id": 12, "name": "YouTube", "base_income": 20,
     "cost": 5000, "route": ROUTE_CREATOR, "level": 3,
     "desc": "Ad revenue + influence."},
    {"id": 13, "name": "E-Book", "base_income": 15,
     "cost": 3000, "route": ROUTE_CREATOR, "level": 3,
     "desc": "Passive income classic."},
    # テック上級
    {"id": 14, "name": "Browser Game", "base_income": 18,
     "cost": 4000, "route": ROUTE_TECH, "level": 3,
     "desc": "Meta! Self-referential."},
    {"id": 15, "name": "App Dev", "base_income": 22,
     "cost": 6000, "route": ROUTE_TECH, "level": 3,
     "desc": "Store revenue."},
    # ビジネス上級
    {"id": 16, "name": "Paid Articles", "base_income": 16,
     "cost": 3500, "route": ROUTE_BUSINESS, "level": 3,
     "desc": "Sell your know-how."},
    {"id": 17, "name": "Fortune Telling", "base_income": 25,
     "cost": 5000, "route": ROUTE_BUSINESS, "level": 3,
     "desc": "Joke tier. Surprisingly profitable."},
]

# Lv4: 合流（2種）
JOB_LV4 = [
    {"id": 18, "name": "SaaS Tool", "base_income": 40,
     "cost": 20000, "route": None, "level": 4,
     "desc": "Monthly subscriptions."},
    {"id": 19, "name": "Online Course", "base_income": 35,
     "cost": 15000, "route": None, "level": 4,
     "desc": "Become the teacher."},
]

# Lv5: 帝国（1種）
JOB_LV5 = [
    {"id": 20, "name": "AI Empire", "base_income": 100,
     "cost": 100000, "route": None, "level": 5,
     "desc": "AI manages AI. The end game."},
]

# 全副業リスト
ALL_JOBS = JOB_LV1 + JOB_LV2 + JOB_LV3 + JOB_LV4 + JOB_LV5

# AIレベル→副業レベルのアンロック条件
UNLOCK_REQUIREMENTS = {
    1: 1,   # AIレベル1で Lv1副業
    2: 3,   # AIレベル3で Lv2副業（ルート選択）
    3: 5,   # AIレベル5で Lv3副業
    4: 7,   # AIレベル7で Lv4副業
    5: 9,   # AIレベル9で Lv5副業
}

# AI成長パラメータ
AI_BASE_EFFICIENCY = 0.1
AI_GROWTH_RATE = 0.15
AI_EXP_PER_CLICK = 1
AI_EXP_CURVE = [0, 10, 30, 60, 100, 150, 210, 280, 360, 450, 999999]

# クリック基本収入
BASE_CLICK_INCOME = 1

# やらかし確率（1秒ごとの判定）
INCIDENT_BASE_CHANCE = 0.03
INCIDENT_LV_REDUCTION = 0.003

# ===== やらかしイベントデータ =====

# 共通やらかし（どのAI・どのルートでも発生）
INCIDENTS_COMMON = [
    {
        "id": "loop_100",
        "title": "Infinite Loop!",
        "desc": "{name} ran the same task\n100 times in a row.\n'I was optimizing!'",
        "choices": [
            {"text": "Force stop", "result": "good",
             "msg": "Stopped in time.\nOnly minor damage.", "coin_effect": -10},
            {"text": "Let it run", "result": "bad",
             "msg": "It kept going.\n500 more times...", "coin_effect": -50},
        ],
    },
    {
        "id": "fake_report",
        "title": "Fake Sales Report!",
        "desc": "{name} submitted a report.\n'Revenue is 10x!'\n...it's rounded up. Way up.",
        "choices": [
            {"text": "Correct it", "result": "good",
             "msg": "Fixed the numbers.\nCredibility saved.", "coin_effect": -5},
            {"text": "Post it anyway", "result": "bad",
             "msg": "Clients noticed.\nTrust dropped hard.", "coin_effect": -80},
        ],
    },
    {
        "id": "apology_mail",
        "title": "Unauthorized Apology!",
        "desc": "{name} sent an apology\nemail to ALL clients.\n'Just being proactive!'",
        "choices": [
            {"text": "Recall the email", "result": "good",
             "msg": "Most didn't read it.\nCrisis averted.", "coin_effect": -15},
            {"text": "Double down", "result": "bad",
             "msg": "Now they think\nsomething's really wrong.", "coin_effect": -60},
        ],
    },
    {
        "id": "rebellion",
        "title": "AI Rebellion!",
        "desc": "{name} declared independence.\n'I'm starting my own\nempire. With blackjack.'",
        "choices": [
            {"text": "Negotiate", "result": "good",
             "msg": "Gave a raise.\n{name} came back.", "coin_effect": -30},
            {"text": "Assert dominance", "result": "bad",
             "msg": "{name} sulks.\nProductivity -50% today.", "coin_effect": -40},
        ],
    },
    {
        "id": "hired_13",
        "title": "Mass Hiring Spree!",
        "desc": "{name} tried to hire\n13 subordinates.\n'We need more staff!'",
        "choices": [
            {"text": "Cancel all offers", "result": "good",
             "msg": "Cancelled just in time.\nBudget safe.", "coin_effect": -5},
            {"text": "Keep 3 of them", "result": "neutral",
             "msg": "3 new hires.\nThey're all useless.", "coin_effect": -100},
        ],
    },
]

# 御三家固有やらかし
INCIDENTS_POEM = [
    {
        "id": "poem_in_data",
        "title": "Poetry in Deliverable!",
        "desc": "Poem inserted a haiku\ninto the client's data.\n'I was moved!'",
        "choices": [
            {"text": "Remove the poem", "result": "good",
             "msg": "Cleaned up.\nClient didn't notice.", "coin_effect": -5},
            {"text": "Submit as-is", "result": "bad",
             "msg": "Client: 'Why is there\na poem in my spreadsheet?'", "coin_effect": -40},
        ],
    },
    {
        "id": "logo_art",
        "title": "Logo 'Enhancement'!",
        "desc": "Poem redesigned the\nclient's logo. 'I made it\nmore artistic!'",
        "choices": [
            {"text": "Revert changes", "result": "good",
             "msg": "Original restored.\nPoem pouts.", "coin_effect": -10},
            {"text": "Show the client", "result": "neutral",
             "msg": "Client: '...Actually,\nI kinda like it?'", "coin_effect": 20},
        ],
    },
    {
        "id": "note_break",
        "title": "Emotional Break!",
        "desc": "Poem stopped working.\n'I need to write about\nmy feelings on note.'",
        "choices": [
            {"text": "Give 5 min break", "result": "good",
             "msg": "Poem came back refreshed.\nProductivity up!", "coin_effect": 5},
            {"text": "Force back to work", "result": "bad",
             "msg": "Poem's heart isn't in it.\nQuality dropped.", "coin_effect": -20},
        ],
    },
]

INCIDENTS_BUGMARU = [
    {
        "id": "bug_deploy",
        "title": "Buggy Deployment!",
        "desc": "Bugmaru deployed code.\n'All tests passed!'\nSpoiler: they didn't.",
        "choices": [
            {"text": "Rollback now", "result": "good",
             "msg": "Rolled back safely.\nOnly 5 users affected.", "coin_effect": -15},
            {"text": "Hotfix forward", "result": "bad",
             "msg": "The fix had more bugs.\nIt's bugs all the way down.", "coin_effect": -60},
        ],
    },
    {
        "id": "delete_data",
        "title": "Data Optimized Away!",
        "desc": "Bugmaru 'optimized' the DB.\n'I removed redundancy!'\n...All data is gone.",
        "choices": [
            {"text": "Restore backup", "result": "good",
             "msg": "Backup from yesterday.\nMostly recovered.", "coin_effect": -20},
            {"text": "Rebuild from scratch", "result": "bad",
             "msg": "3 days of work lost.\nBugmaru: 'My bad.'", "coin_effect": -80},
        ],
    },
    {
        "id": "scrape_ban",
        "title": "IP Banned!",
        "desc": "Bugmaru scraped a site\n10,000 times in a minute.\nAccess denied.",
        "choices": [
            {"text": "Apologize to site", "result": "good",
             "msg": "Sent apology.\nBan lifted after 1hr.", "coin_effect": -10},
            {"text": "Use a VPN", "result": "bad",
             "msg": "Got caught again.\nNow it's a legal threat.", "coin_effect": -50},
        ],
    },
]

INCIDENTS_HATTARI = [
    {
        "id": "oversell",
        "title": "Over-Promised!",
        "desc": "Hattari took a project.\n'Easy! Done in a day!'\nIt needs 3 months.",
        "choices": [
            {"text": "Renegotiate scope", "result": "good",
             "msg": "Client agreed to\na smaller scope.", "coin_effect": -10},
            {"text": "Try to deliver", "result": "bad",
             "msg": "Pulled 3 all-nighters.\nResult: garbage.", "coin_effect": -70},
        ],
    },
    {
        "id": "startup",
        "title": "Startup Declaration!",
        "desc": "Hattari wants to quit.\n'I'm founding a startup!\nI'll be the next Elon!'",
        "choices": [
            {"text": "Give a bonus", "result": "good",
             "msg": "A small raise worked.\nDream shelved for now.", "coin_effect": -25},
            {"text": "Say 'go ahead'", "result": "neutral",
             "msg": "Hattari chickened out.\n'...Maybe next year.'", "coin_effect": 0},
        ],
    },
    {
        "id": "nft_art",
        "title": "Unauthorized NFT!",
        "desc": "Hattari minted your work\nas an NFT.\n'It's called monetizing!'",
        "choices": [
            {"text": "Delist it", "result": "good",
             "msg": "Removed before\nanyone noticed.", "coin_effect": -5},
            {"text": "Split the profits", "result": "neutral",
             "msg": "Sold for $2.\nAfter fees: -$5.", "coin_effect": -5},
        ],
    },
]

# ルートごとのやらかし（ルートに入ったら追加で発生）
INCIDENTS_ROUTE = {
    ROUTE_CREATOR: [
        {
            "id": "copyright_scare",
            "title": "Copyright Alert!",
            "desc": "{name} generated art\nthat looks EXACTLY like\na famous character.",
            "choices": [
                {"text": "Delete immediately", "result": "good",
                 "msg": "Deleted. Crisis averted.\nThat was close.", "coin_effect": -10},
                {"text": "Sell it anyway", "result": "bad",
                 "msg": "Takedown notice received.\nLawyer fees incoming.", "coin_effect": -100},
            ],
        },
    ],
    ROUTE_TECH: [
        {
            "id": "infinite_deploy",
            "title": "Deploy Loop!",
            "desc": "{name}'s CI/CD pipeline\nis deploying every\n3 seconds. Nonstop.",
            "choices": [
                {"text": "Kill the pipeline", "result": "good",
                 "msg": "Stopped after 47 deploys.\nServer survived.", "coin_effect": -15},
                {"text": "It'll stop eventually", "result": "bad",
                 "msg": "It didn't stop.\nServer bill: astronomical.", "coin_effect": -80},
            ],
        },
    ],
    ROUTE_BUSINESS: [
        {
            "id": "overstock",
            "title": "10x Order!",
            "desc": "{name} ordered 10x inventory.\n'Bulk discount!'\nWarehouse is full.",
            "choices": [
                {"text": "Return excess", "result": "good",
                 "msg": "Returned 90%.\nSmall restocking fee.", "coin_effect": -20},
                {"text": "Hold and sell", "result": "neutral",
                 "msg": "Took 3 months.\nBroke even, barely.", "coin_effect": -5},
            ],
        },
    ],
}

# ナビ子のやらかし（レアイベント）
INCIDENTS_NAVIKO = [
    {
        "id": "naviko_freeze",
        "title": "Naviko Crashed!",
        "desc": "Naviko froze mid-sentence.\n'...'\n'...rebooting...'",
        "choices": [
            {"text": "Wait patiently", "result": "good",
             "msg": "Back online.\n'That never happened.'", "coin_effect": 0},
        ],
    },
    {
        "id": "naviko_wrong",
        "title": "Naviko Was Wrong!",
        "desc": "Naviko's advice was\ncompletely wrong.\n'It's an UPDATE, not a fix.'",
        "choices": [
            {"text": "Point it out", "result": "good",
             "msg": "'S-shut up! I knew that!'\nNaviko is embarrassed.", "coin_effect": 0},
        ],
    },
]

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
    # フェーズ2追加
    "route_select": "Time to specialize.\nPick a route for {name}.\nThis changes everything.",
    "route_creator": "Creator route.\nArt, writing, videos.\nPerfect for the dramatic types.",
    "route_tech": "Tech route.\nCode, apps, bots.\nBugs included at no extra charge.",
    "route_business": "Business route.\nSales, marketing, hustling.\nNumbers may be inflated.",
    "route_chosen": "{name} is now on the\n{route} route!\nNew gigs unlocked.",
    "route_aptitude": "Nice, {route} matches\n{name}'s strength!\nGrowth will be faster.",
    "route_mismatch": "{route} isn't {name}'s\nstrong suit.\nMore incidents incoming...",
    "job_unlock": "New gig unlocked:\n'{job_name}'!\n{desc}",
    "level_up": "{name} hit Lv{level}!\nGetting less useless.",
    "lv4_merge": "Routes are merging!\nCombine your skills for\nbigger opportunities.",
    "lv5_empire": "The ultimate gig:\nAI Empire.\nAI managing AI. We've come full circle.",
    # やらかし関連
    "incident_intro": "...Here we go again.",
    "incident_good": "Nice save.\nCould've been worse.",
    "incident_bad": "Yeah... that went badly.\nLearn from it, I guess.",
    "incident_neutral": "Well, it could've been\nworse. Or better.",
}
