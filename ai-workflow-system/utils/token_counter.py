"""
简易 Token 计数器
- 无需 tiktoken 依赖
- 中文按 ~1.5 字/token 估算
- 英文按 ~1.3 词/token 估算
- 用于估算 API 调用消耗
"""

import re


def count_tokens(text):
    """
    估算文本的 token 数量

    Args:
        text: 输入文本（支持中英混合）

    Returns:
        int: 估算的 token 数
    """
    if not text:
        return 0

    # 中文字符（含中文标点）
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', text))
    # 英文字词（按空格拆分）
    english_text = re.sub(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]', ' ', text)
    english_words = len(english_text.split())
    # 数字和特殊字符
    special_chars = len(re.findall(r'[0-9+\-=*/\\|@#$%^&()\[\]{}<>,.;:!?\'\"~`]', text))

    # 估算：中文字符 * 1.5 + 英文词 * 1.3 + 特殊字符 * 0.5
    estimated = int(chinese_chars * 1.5 + english_words * 1.3 + special_chars * 0.5)

    # 至少返回 1
    return max(1, estimated)


def count_messages_tokens(messages):
    """
    估算一组消息的总 token 数

    Args:
        messages: [{"role": "...", "content": "..."}, ...]

    Returns:
        int: 总 token 数
    """
    total = 0
    for msg in messages:
        total += count_tokens(msg.get("role", ""))
        total += count_tokens(msg.get("content", ""))
        total += 3
    return total


def format_token_cost(tokens, price_per_1k_input=0.001, price_per_1k_output=0.002):
    """
    格式化显示 token 费用估算

    Args:
        tokens: token 数量
        price_per_1k_input: 每 1k 输入 token 的价格（美元）
        price_per_1k_output: 每 1k 输出 token 的价格（美元）

    Returns:
        dict: {"tokens": int, "cost_input": float, "cost_output": float, "cost_total": float}
    """
    cost_input = (tokens / 1000) * price_per_1k_input
    cost_output = (tokens / 1000) * price_per_1k_output
    return {
        "tokens": tokens,
        "cost_input": round(cost_input, 6),
        "cost_output": round(cost_output, 6),
        "cost_total": round(cost_input + cost_output, 6),
    }


def print_usage_report(stats):
    """
    打印使用统计报告

    Args:
        stats: {"total_input_tokens": int, "total_output_tokens": int,
                "rounds": int, "agent_calls": int}
    """
    print("\n" + "=" * 50)
    print("Token 使用统计")
    print("=" * 50)
    print("  总输入 Token:   %8d" % stats.get('total_input_tokens', 0))
    print("  总输出 Token:   %8d" % stats.get('total_output_tokens', 0))
    print("  总计 Token:     %8d" % (stats.get('total_input_tokens', 0) + stats.get('total_output_tokens', 0)))
    print("  执行轮次:       %8d" % stats.get('rounds', 0))
    print("  Agent 调用次数: %8d" % stats.get('agent_calls', 0))

    total_input = stats.get('total_input_tokens', 0)
    total_output = stats.get('total_output_tokens', 0)
    input_cost = (total_input / 1000) * 0.001
    output_cost = (total_output / 1000) * 0.002
    print("\n  费用估算 (GPT-3.5 价格)")
    print("  输入费用: $%.4f" % input_cost)
    print("  输出费用: $%.4f" % output_cost)
    print("  总费用:   $%.4f" % (input_cost + output_cost))
    print("=" * 50)
