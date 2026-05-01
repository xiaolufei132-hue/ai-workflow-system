"""
Researcher Agent - 研究分析员
负责对子任务进行深入研究和分析
"""

from agents.base_agent import BaseAgent


class ResearcherAgent(BaseAgent):
    """研究分析员：对子任务进行深入分析"""

    def __init__(self):
        super().__init__("Researcher", "prompts/researcher.txt")

    def run(self, subtask, context=""):
        """
        对子任务进行研究分析

        Args:
            subtask: 子任务描述
            context: 额外的上下文信息（可选）

        Returns:
            str: 研究分析报告
        """
        full_context = f"""子任务：
{subtask}

""" + (f"""额外上下文：
{context}

""" if context else "") + """请针对该子任务进行深入分析，包括：
1. 核心技术要点分析
2. 风险与挑战评估
3. 关键发现与建议"""

        return super().run(full_context)
