"""
Executor Agent - 内容执行器
负责根据研究结果生成具体内容或代码
"""

from agents.base_agent import BaseAgent


class ExecutorAgent(BaseAgent):
    """内容执行器：基于分析结果生成内容"""

    def __init__(self):
        super().__init__("Executor", "prompts/executor.txt")

    def run(self, subtask, research_result, optimization_feedback=""):
        """
        根据研究结果生成内容

        Args:
            subtask: 子任务描述
            research_result: 研究分析结果
            optimization_feedback: 优化反馈（第二轮优化时传入）

        Returns:
            str: 生成的内容/代码
        """
        context = f"""子任务：
{subtask}

研究分析结果：
{research_result}

"""

        if optimization_feedback:
            context += f"""上一轮评审反馈（请针对性改进）：
{optimization_feedback}

"""

        context += """请根据以上信息，生成完整可用的输出内容。"""

        return super().run(context)
