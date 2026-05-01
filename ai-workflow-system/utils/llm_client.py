"""
轻量级 LLM API 客户端
- 支持 OpenAI 兼容的 Chat Completion API
- 通过环境变量配置：LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
- 无需 openai 包，仅用 urllib
- 内置 mock 模式，无 API Key 也能演示流程
"""

import json
import urllib.request
import urllib.error
import os
import time


class LLMClient:
    """轻量级 LLM API 客户端"""

    def __init__(self):
        self.api_key = os.environ.get("LLM_API_KEY", "")
        self.base_url = os.environ.get(
            "LLM_BASE_URL", "https://api.openai.com/v1"
        ).rstrip("/")
        self.model = os.environ.get("LLM_MODEL", "gpt-3.5-turbo")
        self.use_mock = len(self.api_key) < 4
        self.max_retries = 2

    def chat(self, messages, temperature=0.7, max_tokens=2048):
        """
        调用 LLM API 或使用 mock 模式

        Args:
            messages: [{"role": "system"|"user"|"assistant", "content": "..."}]
            temperature: 生成温度
            max_tokens: 最大 token 数

        Returns:
            str: 模型回复内容
        """
        if self.use_mock:
            return self._mock_chat(messages)

        payload = json.dumps({
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        for attempt in range(self.max_retries + 1):
            try:
                req = urllib.request.Request(
                    f"{self.base_url}/chat/completions",
                    data=payload,
                    headers=headers,
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=60) as resp:
                    result = json.loads(resp.read().decode("utf-8"))
                    return result["choices"][0]["message"]["content"]

            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", errors="replace")
                if e.code == 429 and attempt < self.max_retries:
                    wait = min(2 ** (attempt + 1), 10)
                    print(f"  [LLM] 429 限流，等待 {wait}s 后重试...")
                    time.sleep(wait)
                    continue
                print(f"  [LLM] HTTP {e.code}: {body[:200]}")
                print("  [LLM] 切换到 mock 模式")
                self.use_mock = True
                return self._mock_chat(messages)

            except Exception as e:
                print(f"  [LLM] 请求失败: {e}")
                if attempt < self.max_retries:
                    time.sleep(2)
                    continue
                print("  [LLM] 切换到 mock 模式")
                self.use_mock = True
                return self._mock_chat(messages)

        return self._mock_chat(messages)

    def _mock_chat(self, messages):
        """内置 mock 对话，演示系统工作流程"""
        last_msg = messages[-1]["content"] if messages else ""

        # 根据最后一条消息的内容和系统角色判断返回什么
        system_role = ""
        for m in messages:
            if m["role"] == "system":
                system_role = m["content"][:100]
                break

        if "规划" in system_role or "planner" in system_role.lower():
            return self._mock_planner(last_msg)
        elif "研究" in system_role or "researcher" in system_role.lower():
            return self._mock_researcher(last_msg)
        elif "执行" in system_role or "executor" in system_role.lower():
            return self._mock_executor(last_msg)
        elif "评审" in system_role or "reviewer" in system_role.lower():
            return self._mock_reviewer(last_msg)
        else:
            return self._mock_general(last_msg)

    def _mock_planner(self, task):
        return f"""## 任务拆解方案

根据输入任务「{task[:50]}...」，我将其拆解为以下子任务：

### 子任务 1：需求分析与背景调研
- 明确任务的目标和约束条件
- 收集相关背景资料和最佳实践
- 识别关键风险和依赖

### 子任务 2：方案设计与架构规划
- 设计整体解决方案
- 规划技术栈和模块划分
- 制定实施路线图

### 子任务 3：实施与验证
- 按照方案进行实现
- 分阶段验证成果
- 收集反馈并迭代优化

### 执行顺序
子任务1 → 子任务2 → 子任务3

### 预估工作量
- 总工时：约 3 个迭代周期
- 关键里程碑：方案确认 → MVP 交付 → 优化完善"""

    def _mock_researcher(self, task):
        return f"""## 研究分析报告

针对「{task[:50]}...」，已完成以下分析：

### 1. 核心技术点
- 需要重点关注的 3 个关键技术挑战
- 行业内的主流解决方案对比
- 推荐的选型建议和理由

### 2. 风险评估
| 风险项 | 影响程度 | 应对策略 |
|-------|---------|---------|
| 技术复杂度 | 中 | 分阶段实施，降低单次风险 |
| 资源需求 | 低 | 使用现有工具链即可 |
| 时间约束 | 中 | 优先核心功能交付 |

### 3. 关键发现
1. 建议采用模块化设计，便于后续扩展
2. 现有开源生态中有可直接复用的组件
3. 需要特别注意性能优化和异常处理

### 4. 数据来源
- 行业报告分析
- 开源社区调研
- 技术文档参考"""

    def _mock_executor(self, task):
        return f"""## 执行结果

基于任务「{task[:50]}...」，已完成执行：

### 输出概要
1. 完成方案的核心模块设计与实现
2. 包含完整的错误处理机制
3. 提供可扩展的接口设计

### 实现细节

```python
# 核心实现框架
class WorkflowEngine:
    def __init__(self):
        self.tasks = []
        self.results = {{}}
    
    def execute(self, plan):
        for task in plan:
            result = self._process_task(task)
            self.results[task["id"]] = result
        return self.results
    
    def _process_task(self, task):
        # 任务处理逻辑
        task["status"] = "completed"
        return task
```

### 验证结果
- 核心逻辑已完成单元测试
- 接口设计满足可扩展需求
- 性能指标在预期范围内"""

    def _mock_reviewer(self, content):
        return f"""## 评审报告

### 总体评价：需要改进

### 1. 优点
- 整体框架清晰，符合最佳实践
- 核心逻辑完整，覆盖主要场景

### 2. 改进建议

**问题 1：错误处理不够充分**
- 当前版本缺少超时机制
- 建议：添加 try-except 和重试逻辑

**问题 2：可扩展性有待提升**
- 缺少插件化接口设计
- 建议：抽象 Agent 基类，支持自定义 Agent

**问题 3：输出格式需要优化**
- 结果展示不够结构化
- 建议：使用标准化的 JSON 输出格式

### 3. 优化方案
针对以上问题，建议进行 2 轮优化：
1. 第一轮：修复错误处理，增加健壮性
2. 第二轮：优化架构设计，提升扩展性

### 评分
- 完整性：7/10
- 健壮性：6/10
- 可扩展性：6/10
- 总体评价：7/10"""

    def _mock_general(self, content):
        return f"收到任务：{content[:80]}...\n\n已处理完毕。这是 mock 模式下的自动回复。"


# 全局单例
_default_client = None


def get_llm_client():
    """获取全局 LLM 客户端实例"""
    global _default_client
    if _default_client is None:
        _default_client = LLMClient()
    return _default_client
