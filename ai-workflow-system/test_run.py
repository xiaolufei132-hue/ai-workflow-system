"""测试运行"""
import sys
import os
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator import OrchestratorAgent

orchestrator = OrchestratorAgent(optimization_rounds=2)
results = orchestrator.run("写一个Python装饰器，用于记录函数执行时间和参数")
print("\n[OK] 测试通过！")
