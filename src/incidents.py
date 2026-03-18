"""やらかしイベントエンジン"""

import random
from src.constants import (
    INCIDENTS_COMMON, INCIDENTS_POEM, INCIDENTS_BUGMARU, INCIDENTS_HATTARI,
    INCIDENTS_ROUTE, INCIDENTS_NAVIKO,
    INCIDENT_BASE_CHANCE, INCIDENT_LV_REDUCTION,
    AI_POEM, AI_BUGMARU, AI_HATTARI, ROUTE_NONE,
)

# 御三家タイプ→固有やらかしのマッピング
_AI_INCIDENTS = {
    AI_POEM: INCIDENTS_POEM,
    AI_BUGMARU: INCIDENTS_BUGMARU,
    AI_HATTARI: INCIDENTS_HATTARI,
}


class IncidentEngine:
    """やらかしイベントの発生・管理"""

    def __init__(self):
        self.history = []         # 発生済みイベントIDリスト
        self.cooldown = 0         # 連続発生防止（秒）
        self.total_incidents = 0
        self.naviko_incident_chance = 0.005  # ナビ子やらかしは0.5%

    def check_incident(self, ai_agent):
        """毎秒呼ばれる。イベント発生判定。発生したらイベントデータを返す"""
        if self.cooldown > 0:
            self.cooldown -= 1
            return None

        # 基本確率（レベルで減少）
        chance = INCIDENT_BASE_CHANCE - INCIDENT_LV_REDUCTION * (ai_agent.level - 1)
        chance = max(0.005, chance)  # 最低0.5%は残る

        # 適性による倍率
        chance *= ai_agent.incident_multiplier

        if random.random() > chance:
            return None

        # イベント発生！
        event = self._pick_incident(ai_agent)
        if event:
            self.cooldown = 15  # 15秒クールダウン
            self.total_incidents += 1
            self.history.append(event["id"])
            return event
        return None

    def check_naviko_incident(self):
        """ナビ子のやらかし判定（レア）"""
        if random.random() < self.naviko_incident_chance:
            event = random.choice(INCIDENTS_NAVIKO)
            return event
        return None

    def _pick_incident(self, ai_agent):
        """発生するイベントを選択"""
        pool = list(INCIDENTS_COMMON)

        # 御三家固有イベント追加
        ai_incidents = _AI_INCIDENTS.get(ai_agent.ai_type, [])
        pool.extend(ai_incidents)

        # ルートイベント追加
        if ai_agent.route != ROUTE_NONE:
            route_incidents = INCIDENTS_ROUTE.get(ai_agent.route, [])
            pool.extend(route_incidents)

        if not pool:
            return None

        # 最近発生したイベントは確率を下げる（完全除外はしない）
        recent = self.history[-5:] if len(self.history) >= 5 else self.history
        weighted = []
        for event in pool:
            weight = 1.0
            if event["id"] in recent:
                weight = 0.2  # 最近出たものは確率20%に
            weighted.append((event, weight))

        total_weight = sum(w for _, w in weighted)
        r = random.random() * total_weight
        cumulative = 0
        for event, weight in weighted:
            cumulative += weight
            if r <= cumulative:
                return event
        return weighted[-1][0]

    def apply_choice(self, event, choice_index):
        """選択肢の結果を適用。結果dictを返す"""
        if choice_index >= len(event["choices"]):
            choice_index = 0
        choice = event["choices"][choice_index]
        return {
            "result": choice["result"],
            "msg": choice["msg"],
            "coin_effect": choice.get("coin_effect", 0),
        }
