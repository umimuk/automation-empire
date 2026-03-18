"""ゲームロジックのユニットテスト（Phase 2+3対応）"""
import sys
sys.path.insert(0, "/home/umi/.local/lib/python3.12/site-packages")
sys.path.insert(0, "/home/umi/repos/automation-empire")

from src.constants import *
from src.ai_agent import AIAgent
from src.jobs import JobManager
from src.incidents import IncidentEngine
from src.text_util import format_number

print("=== AIAgent Tests ===")

# 基本テスト
agent = AIAgent(AI_POEM)
assert agent.name == "Poem"
assert agent.level == 1
assert agent.aptitude_route == ROUTE_CREATOR
assert agent.route == ROUTE_NONE
print(f"  Agent: {agent.name}, aptitude={ROUTE_NAMES[agent.aptitude_route]}")

# ルート設定テスト
agent.set_route(ROUTE_CREATOR)
assert agent.route == ROUTE_CREATOR
assert agent.growth_multiplier == APTITUDE_BONUS
assert agent.incident_multiplier == APTITUDE_INCIDENT_BONUS
print(f"  Aptitude match: growth={agent.growth_multiplier}x, incident={agent.incident_multiplier}x")

# 苦手ルートテスト
agent2 = AIAgent(AI_POEM)
agent2.set_route(ROUTE_BUSINESS)  # Poem's opposite
assert agent2.growth_multiplier == APTITUDE_PENALTY
assert agent2.incident_multiplier == APTITUDE_INCIDENT_PENALTY
print(f"  Mismatch: growth={agent2.growth_multiplier}x, incident={agent2.incident_multiplier}x")

# レベルアップテスト
agent3 = AIAgent(AI_BUGMARU)
for _ in range(15):
    agent3.add_exp(1)
assert agent3.level == 2
print(f"  Leveling: Lv{agent3.level}, exp={agent3.exp}")

# Lv10テスト
agent4 = AIAgent(AI_HATTARI)
agent4.level = 10
assert agent4.exp_progress == 1.0
print(f"  Lv10: progress={agent4.exp_progress}")

print("=== JobManager Tests ===")

jm = JobManager()

# 初期状態
available = jm.get_available_jobs(1, ROUTE_NONE)
lv1_available = [j for j in available if j["level"] == 1]
assert len(lv1_available) == 3, f"Expected 3 Lv1 jobs, got {len(lv1_available)}"
print(f"  Lv1 available: {len(lv1_available)} jobs")

# 購入テスト
result = jm.buy_job(0, 100)  # Data Entry, cost=0
assert result is not None
assert result[0] == 100  # coins unchanged
print(f"  Bought Data Entry, coins left: {result[0]}")

# 重複購入不可
result2 = jm.buy_job(0, 100)
assert result2 is None
print("  Duplicate buy blocked: OK")

# ルート選択前はLv2買えない
available_no_route = jm.get_available_jobs(3, ROUTE_NONE)
lv2_in_list = [j for j in available_no_route if j["level"] == 2]
assert len(lv2_in_list) == 0
print("  Lv2 blocked without route: OK")

# ルート選択後
available_creator = jm.get_available_jobs(3, ROUTE_CREATOR)
lv2_creator = [j for j in available_creator if j["level"] == 2]
assert len(lv2_creator) == 3  # Blog, AI Art, Short Videos
print(f"  Lv2 Creator route: {len(lv2_creator)} jobs available")
for j in lv2_creator:
    print(f"    - {j['name']} (+{j['base_income']}/c, ${j['cost']})")

# ルート必要性チェック
assert jm.needs_route_selection(3, ROUTE_NONE) == True
assert jm.needs_route_selection(3, ROUTE_CREATOR) == False
assert jm.needs_route_selection(2, ROUTE_NONE) == False
print("  Route selection check: OK")

print("=== IncidentEngine Tests ===")

ie = IncidentEngine()
test_agent = AIAgent(AI_POEM)
test_agent.set_route(ROUTE_CREATOR)

# イベント発生テスト（確率なので複数回試行）
triggered = 0
for _ in range(1000):
    event = ie.check_incident(test_agent)
    if event:
        triggered += 1
        ie.cooldown = 0  # テスト用にクールダウンリセット
print(f"  Incidents in 1000 checks: {triggered} (aptitude route = lower rate)")

# 苦手ルートでのテスト
ie2 = IncidentEngine()
test_agent2 = AIAgent(AI_POEM)
test_agent2.set_route(ROUTE_BUSINESS)
triggered2 = 0
for _ in range(1000):
    event = ie2.check_incident(test_agent2)
    if event:
        triggered2 += 1
        ie2.cooldown = 0
print(f"  Incidents mismatch route: {triggered2} (should be higher)")
assert triggered2 > triggered, "Mismatch route should have more incidents"

# Bugmaru苦手ルートテスト（Tech適性 → Business苦手）
bugmaru = AIAgent(AI_BUGMARU)
bugmaru.set_route(ROUTE_BUSINESS)
assert bugmaru.growth_multiplier == 0.7, f"Bugmaru weakness should be 0.7, got {bugmaru.growth_multiplier}"
assert bugmaru.incident_multiplier == 2.0, f"Bugmaru incident penalty should be 2.0, got {bugmaru.incident_multiplier}"
bugmaru_normal = AIAgent(AI_BUGMARU)
bugmaru_normal.set_route(ROUTE_CREATOR)
assert bugmaru_normal.growth_multiplier == 1.0, f"Bugmaru Creator should be normal 1.0, got {bugmaru_normal.growth_multiplier}"
print(f"  Bugmaru weakness test: Business=0.7x/2.0x, Creator=1.0x OK")

# 選択肢適用テスト
test_event = INCIDENTS_COMMON[0]
result = ie.apply_choice(test_event, 0)
assert "result" in result
assert "coin_effect" in result
print(f"  Choice test: result={result['result']}, effect={result['coin_effect']}")

print("=== Format Tests ===")
assert format_number(999) == "999"
assert format_number(1500) == "1.5K"
assert format_number(2000000) == "2.0M"
print("  Number formatting: OK")

print("\n=== ALL TESTS PASSED! ===")
print(f"Total jobs defined: {len(ALL_JOBS)}")
print(f"  Lv1: {len(JOB_LV1)}, Lv2: {len(JOB_LV2)}, Lv3: {len(JOB_LV3)}, "
      f"Lv4: {len(JOB_LV4)}, Lv5: {len(JOB_LV5)}")
print(f"Total incidents: common={len(INCIDENTS_COMMON)}, "
      f"poem={len(INCIDENTS_POEM)}, bugmaru={len(INCIDENTS_BUGMARU)}, "
      f"hattari={len(INCIDENTS_HATTARI)}")
