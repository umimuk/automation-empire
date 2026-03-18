"""ゲームロジックのユニットテスト"""
import sys
sys.path.insert(0, "/home/umi/.local/lib/python3.12/site-packages")
sys.path.insert(0, "/home/umi/repos/automation-empire")

from src.constants import *
from src.ai_agent import AIAgent
from src.text_util import format_number

# AIエージェントテスト
agent = AIAgent(0)
assert agent.name == AI_NAMES_DEFAULT[0], f"Expected default name, got {agent.name}"
assert agent.level == 1
assert agent.efficiency == 0.1

# 名前変更テスト
agent.rename("MyAI")
assert agent.name == "MyAI"

# 経験値テスト
for i in range(15):
    agent.add_exp(1)
assert agent.level == 2, f"Expected Lv2, got Lv{agent.level}"
assert agent.exp == 5, f"Expected 5 exp, got {agent.exp}"

# フォーマットテスト
assert format_number(999) == "999"
assert format_number(1500) == "1.5K"
assert format_number(2000000) == "2.0M"

print("All tests passed!")
print(f"Agent: {agent.name} Lv{agent.level} ({agent.type_name})")
print(f"Efficiency: {agent.efficiency:.2f}")
print(f"Auto income: {agent.auto_income:.2f}/s")
print(f"Tutorial messages: {len(TUTORIAL_MESSAGES)}")
print(f"Lv1 jobs: {len(JOB_LV1)}")
