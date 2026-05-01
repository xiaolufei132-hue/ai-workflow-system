"""
Reviewer Agent - 质量评审员
负责审核执行结果并提供优化建议
"""

from agents.base_agent import BaseAgent


class ReviewerAgent(BaseAgent):
    """质量评审员：评审输出质量并提供优化建议"""

    def __init__(self):
        super().__init__("Reviewer", "prompts/reviewer.txt")

    def run(self, subtask, execution_result, round_num=1):
        """
        评审执行结果

        Args:
            subtask: 子任务描述
            execution_result: 执行器输出的结果
            round_num: 当前评审轮次（第几轮）

        Returns:
            str: 评审报告和改进建议
        """
        context = f"""子任务：
{subtask}

执行结果（第 {round_num} 轮）：
{execution_result}

请评审该执行结果的质量，指出问题并给出具体的改进建议。"""

        return super().run(context)
