# 🤖 AI Workflow System

> **多 Agent 协同 · 自动拆解 · 多轮优化 · 循环执行**

基于多 Agent 协同的 AI 工作流自动化系统。输入一个任务，系统自动完成**拆解→研究→执行→评审→优化**的完整闭环。

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🧩 **自动拆解** | 将复杂任务自动分解为多个子任务 |
| 👥 **多 Agent 协同** | Planner → Researcher → Executor → Reviewer 有序协作 |
| 🔄 **多轮优化** | 每个子任务至少经过 2 轮"执行→评审→改进"循环 |
| 📊 **Token 统计** | 内置 Token 计数器和费用估算 |
| ⚡ **零依赖运行** | 无需安装 openai 包，仅依赖 Python 标准库 + requests（可选） |
| 🎭 **Mock 模式** | 未配置 API Key 也能演示完整工作流程 |

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    Orchestrator                         │
│                    (主控制器)                            │
└──┬────────┬────────┬────────┬────────┬──────────────────┘
   │        │        │        │        │
   ▼        ▼        ▼        ▼        ▼
┌─────┐ ┌──────┐ ┌────────┐ ┌──────┐ ┌──────────┐
│Plan-│ │Research│ │Execu- │ │Review│ │  Token   │
│ner  │ │-er    │ │-tor   │ │-er   │ │ Counter  │
└─────┘ └──────┘ └────────┘ └──────┘ └──────────┘
 拆解     研究     执行     评审     统计
```

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/your-username/ai-workflow-system.git
cd ai-workflow-system

# 安装依赖（可选 - 不装也能用 mock 模式）
pip install requests
```

### 配置 API Key（可选）

```bash
# 如果要用真实 LLM API（兼容 OpenAI 格式）
export LLM_API_KEY="your-api-key-here"        # Windows: set LLM_API_KEY=...
export LLM_BASE_URL="https://api.openai.com/v1"  # 可选，默认 OpenAI
export LLM_MODEL="gpt-3.5-turbo"                 # 可选，默认 gpt-3.5-turbo
```

> 不配置 API Key → 自动使用 **Mock 模式**，内置智能回复，可演示完整流程。

### 运行

```bash
# 方式一：命令行传参
python main.py "设计一个基于Python的简易Web框架，支持路由、中间件和模板渲染"

# 方式二：交互式输入
python main.py
# 然后粘贴或输入你的任务，两次回车结束
```

## 📋 示例任务

以下是一些完整可运行的任务示例：

### 示例 1：技术方案设计
```bash
python main.py "为一个小型电商系统设计微服务架构方案"
```

### 示例 2：内容创作
```bash
python main.py "写一篇关于AI Agent发展趋势的分析文章，面向技术管理者"
```

### 示例 3：代码生成
```bash
python main.py "实现一个Python装饰器，用于记录函数执行时间和参数"
```

### 示例 4：文档编写
```bash
python main.py "编写MySQL数据库的设计规范文档，包含命名规范、索引设计和SQL编写规范"
```

### 示例 5：项目管理
```bash
python main.py "制定一个3个月的Web应用开发计划，包含里程碑和交付物"
```

## 🔄 系统工作流程

```
用户输入任务
    │
    ▼
┌─────────────────────┐
│  1. Planner Agent   │  ← 拆解任务为 2-4 个子任务
│  (任务规划器)       │
└─────────┬───────────┘
          │
          ▼  (对每个子任务循环)
┌─────────────────────┐
│  2. Researcher Agent│  ← 深入分析子任务
│  (研究分析员)       │     识别风险/关键点
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  3. Executor Agent  │  ← 生成内容/代码
│  (内容执行器)       │
└─────────┬───────────┘
          │
          ▼  ┌─────────────────────┐
             │ 4. Reviewer Agent  │  ← 评审质量
             │ (质量评审员)       │     给出改进建议
             └─────────┬───────────┘
                       │
          ┌────────────┴────────────┐
          │                         │
    还有优化轮次？             无需优化
          │                         │
          ▼                         ▼
  回到 Executor             输出最终结果
  根据反馈改进
```

### 关键流程说明

1. **拆解阶段**：将复杂任务分解为 2-4 个独立可执行的子任务
2. **研究阶段**：对每个子任务进行深度分析，识别技术要点和风险
3. **执行阶段**：基于研究成果生成具体的内容或代码
4. **评审阶段**：审核执行结果，给出具体改进建议
5. **优化循环**：每个子任务至少经过 2 轮"执行→评审→改进"的循环

## 📁 项目结构

```
ai-workflow-system/
├── main.py                 # 程序入口
├── README.md               # 本文档
├── requirements.txt        # 依赖清单
├── agents/                 # Agent 模块
│   ├── __init__.py
│   ├── base_agent.py       # Agent 基类
│   ├── orchestrator.py     # 主控制器（编排流程）
│   ├── planner.py          # 任务规划器
│   ├── researcher.py       # 研究分析员
│   ├── executor.py         # 内容执行器
│   └── reviewer.py         # 质量评审员
├── prompts/                # Prompt 模板
│   ├── __init__.py
│   ├── planner.txt
│   ├── researcher.txt
│   ├── executor.txt
│   └── reviewer.txt
└── utils/                  # 工具模块
    ├── __init__.py
    ├── llm_client.py       # LLM API 客户端
    └── token_counter.py    # Token 计数器
```

## 📊 Token 消耗说明

### 高频使用场景 Token 估算

| 任务类型 | 子任务数 | 优化轮次 | 预估 Token | 预估费用 |
|---------|:-------:|:--------:|:----------:|:--------:|
| 技术方案设计 | 3 | 2 | ~12,000 | ~$0.02 |
| 代码生成 | 2 | 2 | ~8,000 | ~$0.01 |
| 文档编写 | 3 | 2 | ~15,000 | ~$0.03 |
| 综合创意任务 | 4 | 3 | ~25,000 | ~$0.05 |

> 以上按 GPT-3.5 价格估算（$0.001/1K 输入，$0.002/1K 输出）

### Token 构成

```
单次调用 = 系统 Prompt + 用户输入 + Agent 输出
每个子任务循环 = 研究 + (执行 + 评审) × 优化轮数
总 Token = 单次调用 × (Planner + Researcher + Executor + Reviewer × 轮数) × 子任务数
```

### Mock 模式

未配置 API Key 时，系统自动使用内置的 Mock 回复。Mock 模式下的回复包含了完整的结构化示例输出，让你可以零成本体验整个工作流程。

## 🛠️ 技术细节

- **纯 Python 实现**：无外部框架依赖
- **轻量 HTTP 客户端**：基于 `urllib`，兼容 OpenAI API 格式
- **内置 Token 计数器**：无需 tiktoken，支持中英文混合估算
- **自动降级**：API 失败自动切换到 Mock 模式

## 📄 License

MIT License
