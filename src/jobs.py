"""副業管理システム"""

from src.constants import (
    ALL_JOBS, JOB_LV1, JOB_LV2, JOB_LV3, JOB_LV4, JOB_LV5,
    UNLOCK_REQUIREMENTS, ROUTE_NONE,
)


class JobManager:
    """副業のアンロック・管理"""

    def __init__(self):
        self.owned_jobs = []       # 購入済み副業IDリスト
        self.active_jobs = []      # 稼働中の副業IDリスト

    def get_available_jobs(self, ai_level, route):
        """現在アンロック可能な副業一覧を返す（未購入のみ）"""
        available = []
        for job in ALL_JOBS:
            if job["id"] in self.owned_jobs:
                continue
            # レベル条件チェック
            required_ai_lv = UNLOCK_REQUIREMENTS.get(job["level"], 99)
            if ai_level < required_ai_lv:
                continue
            # ルート条件チェック
            if job["route"] is not None:
                if route == ROUTE_NONE:
                    continue  # ルート未選択なのにルート副業は買えない
                if job["route"] != route and job["level"] <= 3:
                    continue  # Lv2-3は選択ルートのみ
            available.append(job)
        return available

    def buy_job(self, job_id, coins):
        """副業を購入。成功したら(残りコイン, job)を返す。失敗はNone"""
        job = self.get_job(job_id)
        if job is None or job_id in self.owned_jobs:
            return None
        if coins < job["cost"]:
            return None
        self.owned_jobs.append(job_id)
        self.active_jobs.append(job_id)
        return (coins - job["cost"], job)

    def get_job(self, job_id):
        """IDから副業データを取得"""
        for job in ALL_JOBS:
            if job["id"] == job_id:
                return job
        return None

    def get_owned_jobs(self):
        """購入済み副業のデータリストを返す"""
        return [self.get_job(jid) for jid in self.owned_jobs if self.get_job(jid)]

    def calc_click_bonus(self):
        """稼働中副業のクリックボーナス合計"""
        total = 0
        for jid in self.active_jobs:
            job = self.get_job(jid)
            if job:
                total += job["base_income"]
        return total

    def calc_auto_bonus(self):
        """稼働中副業の自動収入ボーナス（副業数に応じた倍率）"""
        return len(self.active_jobs)

    def needs_route_selection(self, ai_level, route):
        """ルート選択が必要かチェック"""
        required = UNLOCK_REQUIREMENTS.get(2, 3)
        return ai_level >= required and route == ROUTE_NONE

    def get_highest_job_level(self):
        """所持している副業の最高レベル"""
        if not self.owned_jobs:
            return 0
        max_lv = 0
        for jid in self.owned_jobs:
            job = self.get_job(jid)
            if job and job["level"] > max_lv:
                max_lv = job["level"]
        return max_lv
