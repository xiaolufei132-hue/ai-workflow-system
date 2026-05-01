"""
Agent 基类 - 所有 Agent 的父类
"""

import os
from utils.llm_client import get_llm_client
from utils.token_counter import count_tokens


class BaseAgent:
    """所有 Agent 的基类"""

    def __init__(self, name, prompt_path):
        """
        Args:
            name: Agent 名称
            prompt_path: prompt 文件路径
        """
        self.name = name
        self.llm = get_llm_client()
        self.system_prompt = self._load_prompt(prompt_path)
        self.call_count = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0

    def _load_prompt(self, path):
        """从文件加载系统 prompt"""
        full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            return f"你是 {self.name} Agent，请执行你的职责。"

    def run(self, context, max_retries=1):
        """
        执行 Agent 任务

        Args:
            context: 上下文信息（字符串或消息列表）
            max_retries: 最大重试次数

        Returns:
            str: Agent 的输出内容
        """
        if isinstance(context, str):
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": context},
            ]
        else:
            messages = context

        # 统计输入 token
        input_tokens = 0
        for m in messages:
            input_tokens += count_tokens(m.get("content", ""))

        self.call_count += 1
        self.total_input_tokens += input_tokens

        # 调用 LLM
        result = self.llm.chat(messages)

        # 统计输出 token
        output_tokens = count_tokens(result)
        self.total_output_tokens += output_tokens

        return result

    def get_stats(self):
        """获取使用统计"""
        return {
            "calls": self.call_count,
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
        }

    def get_name(self):
        return self.name
