"""
Orchestrator Agent - 主控制器
负责协调整个工作流程：调度所有 Agent，管理执行循环
"""

from agents.planner import PlannerAgent
from agents.researcher import ResearcherAgent
from agents.executor import ExecutorAgent
from agents.reviewer import ReviewerAgent
from utils.token_counter import print_usage_report


class OrchestratorAgent:
    """主控制器：编排整个多 Agent 工作流程"""

    def __init__(self, optimization_rounds=2):
        """
        Args:
            optimization_rounds: 每轮子任务的优化轮数（默认 2 轮）
        """
        self.planner = PlannerAgent()
        self.researcher = ResearcherAgent()
        self.executor = ExecutorAgent()
        self.reviewer = ReviewerAgent()
        self.optimization_rounds = max(2, optimization_rounds)

        # 总统计
        self.total_rounds = 0
        self.total_agent_calls = 0
        self.final_results = {}

    def run(self, task_description):
        """
        执行完整的工作流程

        Args:
            task_description: 用户输入的任务描述

        Returns:
            dict: 执行结果，包含各阶段输出
        """
        print("\n" + "=" * 60)
        print("== AI Workflow System 启动 ==")
        print("=" * 60)
        print("输入任务:", task_description)
        print("每轮优化次数:", self.optimization_rounds)
        print("=" * 60)

        # ========== 阶段 1：规划（Planner） ==========
        print("\n[阶段 1/4] Planner - 任务拆解规划")
        print("-" * 40)
        plan = self.planner.run(task_description)
        print(plan)
        self.total_agent_calls += 1

        # 解析子任务
        subtasks = self.planner.parse_subtasks(plan)
        print("\n拆解出", len(subtasks), "个子任务")
        for i, st in enumerate(subtasks):
            title = st.split("\n")[0] if "\n" in st else st[:60]
            print("  [" + str(i + 1) + "]", title)

        # ========== 阶段 2-4：对每个子任务执行研究 -> 执行 -> 评审 -> 优化循环 ==========
        for idx, subtask in enumerate(subtasks):
            print("\n" + "=" * 50)
            print("== [子任务", idx + 1, "/", len(subtasks), "] ==")
            print("=" * 50)

            # ---------- 子阶段 A：研究 ----------
            print("\n[阶段 2/4] Researcher - 研究分析")
            print("-" * 40)
            research = self.researcher.run(subtask)
            print(research)
            self.total_agent_calls += 1

            # ---------- 子阶段 B：执行 ----------
            print("\n[阶段 3/4] Executor - 内容生成")
            print("-" * 40)
            execution = self.executor.run(subtask, research)
            print(execution)
            self.total_agent_calls += 1

            # ---------- 子阶段 C：评审 + 优化循环 ----------
            current_result = execution
            for round_num in range(1, self.optimization_rounds + 1):
                print("\n[优化轮次", round_num, "/", self.optimization_rounds, "]")
                print("-" * 40)

                # 评审
                print("\n[阶段 4/4] Reviewer - 质量评审")
                review = self.reviewer.run(subtask, current_result, round_num)
                print(review)
                self.total_agent_calls += 1
                self.total_rounds += 1

                if round_num < self.optimization_rounds:
                    # 优化：重新执行
                    print("\n[优化] Executor - 根据反馈改进")
                    current_result = self.executor.run(
                        subtask, research,
                        optimization_feedback=review
                    )
                    print(current_result)
                    self.total_agent_calls += 1
                else:
                    current_result = current_result + "\n\n---\n\n## 评审反馈（第 " + str(round_num) + " 轮）\n" + review

            # 保存该子任务的最终结果
            self.final_results["subtask_" + str(idx + 1)] = {
                "subtask": subtask,
                "research": research,
                "execution": current_result,
            }

        # ========== 输出最终报告 ==========
        self._print_final_report(task_description)
        self._print_stats()

        return self.final_results

    def _print_final_report(self, task_description):
        """打印最终执行报告"""
        print("\n" + "=" * 60)
        print("== 最终执行报告 ==")
        print("=" * 60)
        print("任务:", task_description)
        print("子任务数:", len(self.final_results))
        print("执行轮次:", self.total_rounds)
        print("\n各子任务结果:")
        for key, value in self.final_results.items():
            first_line = value["subtask"].split("\n")[0] if "\n" in value["subtask"] else value["subtask"][:60]
            print("  [" + key + "]", first_line)
            print("    -> 研究分析:", len(value["research"]), "字符")
            print("    -> 执行输出:", len(value["execution"]), "字符")
        print("=" * 60)

    def _print_stats(self):
        """打印所有 Agent 的使用统计"""
        agents = [
            ("Planner", self.planner.get_stats()),
            ("Researcher", self.researcher.get_stats()),
            ("Executor", self.executor.get_stats()),
            ("Reviewer", self.reviewer.get_stats()),
        ]

        total_input = sum(s["input_tokens"] for _, s in agents)
        total_output = sum(s["output_tokens"] for _, s in agents)

        stats = {
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "rounds": self.total_rounds,
            "agent_calls": self.total_agent_calls,
        }

        print("Agent 级统计:")
        header = "  %-15s %-10s %-12s %-12s" % ("Agent", "调用次数", "输入Token", "输出Token")
        print(header)
        print("  " + "-" * 49)
        for name, s in agents:
            print("  %-15s %-10d %-12d %-12d" % (name, s["calls"], s["input_tokens"], s["output_tokens"]))

        print_usage_report(stats)
