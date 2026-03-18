"""御三家AIエージェントクラス"""

from src.constants import (
    AI_NAMES_DEFAULT, AI_TYPES, AI_COLORS,
    AI_BASE_EFFICIENCY, AI_GROWTH_RATE,
    AI_EXP_PER_CLICK, AI_EXP_CURVE,
    AI_APTITUDE, AI_WEAKNESS, ROUTE_NONE,
    APTITUDE_BONUS, APTITUDE_NORMAL, APTITUDE_PENALTY,
    APTITUDE_INCIDENT_BONUS, APTITUDE_INCIDENT_PENALTY,
)


class AIAgent:
    """御三家AIエージェント"""

    def __init__(self, ai_type):
        self.ai_type = ai_type  # 0=ポエム, 1=バグ丸, 2=ハッタリ
        self.name = AI_NAMES_DEFAULT[ai_type]
        self.type_name = AI_TYPES[ai_type]
        self.color = AI_COLORS[ai_type]
        self.level = 1
        self.exp = 0
        self.total_earned = 0
        self.incident_count = 0
        self.route = ROUTE_NONE  # 未選択
        self.aptitude_route = AI_APTITUDE[ai_type]  # 得意ルート

    @property
    def efficiency(self):
        """自動収入の効率（レベルに応じて上昇、適性でボーナス）"""
        base = AI_BASE_EFFICIENCY + AI_GROWTH_RATE * (self.level - 1)
        return base * self.growth_multiplier

    @property
    def growth_multiplier(self):
        """ルート適性による成長倍率"""
        if self.route == ROUTE_NONE:
            return APTITUDE_NORMAL
        if self.route == self.aptitude_route:
            return APTITUDE_BONUS
        # 苦手判定（明示的な苦手ルート定義）
        weakness = AI_WEAKNESS.get(self.ai_type)
        if weakness is not None and self.route == weakness:
            return APTITUDE_PENALTY
        return APTITUDE_NORMAL

    @property
    def incident_multiplier(self):
        """やらかし確率倍率（適性で変動）"""
        if self.route == ROUTE_NONE:
            return 1.0
        if self.route == self.aptitude_route:
            return APTITUDE_INCIDENT_BONUS
        weakness = AI_WEAKNESS.get(self.ai_type)
        if weakness is not None and self.route == weakness:
            return APTITUDE_INCIDENT_PENALTY
        return 1.0

    @property
    def auto_income(self):
        """1秒あたりの自動収入"""
        return self.efficiency * self.level

    @property
    def exp_to_next(self):
        """次のレベルまでの必要経験値"""
        if self.level >= len(AI_EXP_CURVE):
            return 999999
        return AI_EXP_CURVE[self.level]

    @property
    def exp_progress(self):
        """現在の経験値の進捗率 (0.0-1.0)"""
        if self.level >= 10:
            return 1.0
        needed = self.exp_to_next
        if needed <= 0:
            return 1.0
        return min(1.0, self.exp / needed)

    def add_exp(self, amount):
        """経験値を追加。レベルアップしたらTrueを返す"""
        adjusted = int(amount * self.growth_multiplier)
        self.exp += max(1, adjusted)
        leveled_up = False
        while self.exp >= self.exp_to_next and self.level < 10:
            self.exp -= self.exp_to_next
            self.level += 1
            leveled_up = True
        return leveled_up

    def set_route(self, route):
        """ルートを設定"""
        self.route = route

    def rename(self, new_name):
        """名前変更"""
        if new_name.strip():
            self.name = new_name.strip()[:8]
