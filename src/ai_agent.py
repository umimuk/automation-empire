"""御三家AIエージェントクラス"""

from src.constants import (
    AI_NAMES_DEFAULT, AI_TYPES, AI_COLORS,
    AI_BASE_EFFICIENCY, AI_GROWTH_RATE,
    AI_EXP_PER_CLICK, AI_EXP_CURVE,
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

    @property
    def efficiency(self):
        """自動収入の効率（レベルに応じて上昇）"""
        return AI_BASE_EFFICIENCY + AI_GROWTH_RATE * (self.level - 1)

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
        needed = self.exp_to_next
        if needed <= 0:
            return 1.0
        return min(1.0, self.exp / needed)

    def add_exp(self, amount):
        """経験値を追加。レベルアップしたらTrueを返す"""
        self.exp += amount
        leveled_up = False
        while self.exp >= self.exp_to_next and self.level < 10:
            self.exp -= self.exp_to_next
            self.level += 1
            leveled_up = True
        return leveled_up

    def rename(self, new_name):
        """名前変更"""
        if new_name.strip():
            self.name = new_name.strip()[:8]  # 最大8文字
