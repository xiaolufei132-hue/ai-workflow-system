"""
AI Workflow System - 多Agent协同的AI工作流自动化系统

入口文件
支持两种模式：
1. 命令行参数：python main.py "你的任务描述"
2. 交互模式：python main.py（然后输入任务）
"""

import sys
import os
import io

# 修复 Windows 控制台编码问题
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.orchestrator import OrchestratorAgent


def print_banner():
    """打印启动横幅"""
    print("""
    ============================================
        AI Workflow System v1.0
        多 Agent 协同 | 自动拆解 | 循环优化
    ============================================
    """)


def main():
    """主入口"""
    print_banner()

    # 获取任务描述
    if len(sys.argv) > 1:
        task_description = " ".join(sys.argv[1:])
        print("从命令行获取任务:", task_description)
    else:
        print("请输入任务描述（输入完成后按两次回车）：")
        lines = []
        try:
            while True:
                line = input()
                if line.strip() == "" and lines and lines[-1].strip() == "":
                    break
                lines.append(line)
        except (EOFError, KeyboardInterrupt):
            pass
        task_description = "\n".join(lines).strip()

        if not task_description:
            # 使用默认示例任务
            task_description = "设计一个基于Python的简易Web框架，支持路由、中间件和模板渲染"
            print("\n未输入任务，使用默认示例:")
            print("  ", task_description)

    # 创建编排器并执行
    orchestrator = OrchestratorAgent(optimization_rounds=2)

    try:
        results = orchestrator.run(task_description)
        print("\n工作流执行完成！")
        return 0
    except KeyboardInterrupt:
        print("\n\n用户中断执行")
        return 1
    except Exception as e:
        print("\n执行出错:", e)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
