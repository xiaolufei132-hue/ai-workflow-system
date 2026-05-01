"""
Planner Agent - 任务拆解规划器
负责将用户输入的任务拆解为可执行的子任务
"""

from agents.base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    """任务规划器：分析任务并拆解为子任务"""

    def __init__(self):
        super().__init__("Planner", "prompts/planner.txt")

    def run(self, task_description):
        """
        将任务拆解为子任务

        Args:
            task_description: 用户输入的原始任务描述

        Returns:
            str: 包含子任务规划的 Markdown 文本
        """
        context = f"""请对以下任务进行拆解和规划：

任务描述：
{task_description}

请分析任务需求，将其拆解为 2-4 个可执行的子任务，并指定执行顺序和依赖关系。"""

        return super().run(context)

    def parse_subtasks(self, plan_text):
        """
        从规划文本中提取子任务列表（简单解析）

        Args:
            plan_text: Planner 输出的规划文本

        Returns:
            list: 子任务描述列表
        """
        lines = plan_text.strip().split("\n")
        subtasks = []
        current_task = ""

        for line in lines:
            line = line.strip()
            # 识别子任务标题（如 "### 子任务 1：xxx"）
            if line.startswith("###") and ("子任务" in line or "subtask" in line.lower()):
                if current_task:
                    subtasks.append(current_task.strip())
                current_task = line + "\n"
            elif current_task:
                current_task += line + "\n"

        if current_task:
            subtasks.append(current_task.strip())

        # 如果解析不到，把全部内容作为唯一子任务
        if not subtasks:
            subtasks = [plan_text]

        return subtasks
