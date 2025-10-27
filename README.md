# LangChain核心组件
1️⃣ Models（模型层）：LangChain 的基础：一切都围绕模型调用展开。（LLM、Chat、Embeddings）

2️⃣ Prompts（提示词模板）：用于管理「输入格式化」与「上下文组合」。

3️⃣ Chains（链式调用）：Chains 是 LangChain 最早期的核心概念， 用于把「Prompt + Model + Output 处理」组合成一个可复用的逻辑链。

1. extend/sequential chains（扩展/顺序链）：将多个 Chains 串联起来，形成更复杂的逻辑。
2. parallel chains（并行链）：同时调用多个 Chains，并将结果合并。
   1. 以不同的方式在不同的链上执行相似的任务
   2. 同一个任务划分为多个子任务，在不同的链上并行处理
3. conditional chains（条件链）：根据条件选择不同的 Chains 执行路径。

4️⃣ Memory（记忆模块）：保存历史对话，用于多轮上下文。

5️⃣ Tools & Agents（工具与智能体）：LangChain 允许 LLM 动态调用外部工具（比如搜索、数据库、计算器等）。
    🔧 Tools（工具）：工具是封装好的功能函数，可被智能体调用。
    🧠 Agents（智能体）：智能体是一个“思考-行动-再思考”的循环系统：

6️⃣ Runnables（LangChain 1.0 新核心）

🚀 二、LangChain 1.0 的核心组件结构

LangChain 1.0 可以分为 七大核心组件：

模块	主要类	功能简述
1️⃣ Prompts（提示模板）	ChatPromptTemplate, PromptTemplate, MessagesPlaceholder	管理系统提示词、人类提示词等，支持参数化模板。

2️⃣ Models（模型接口）	ChatOpenAI, ChatAnthropic, ChatDeepSeek 等	封装LLM模型的调用接口，统一输入输出结构。

3️⃣ Output Parsers（输出解析器）	StrOutputParser, StructuredOutputParser, PydanticOutputParser	将模型输出解析为字符串、结构化数据或JSON等。

4️⃣ Runnables（可运行单元）	RunnableLambda, RunnableParallel, RunnableSequence, RunnableWithMessageHistory	1.0的核心抽象，用于构建、并行执行、分支、消息记忆等。

5️⃣ Memory（记忆）	MongoDBChatMessageHistory, ConversationBufferMemory	保存上下文历史，配合 RunnableWithMessageHistory 使用。

6️⃣ Chains（链式组合）	任意 Runnable 组合而成	通过 `

7️⃣ Tools / Agents（工具与代理）	Tool, AgentExecutor, RunnableAgent	用于扩展功能，如检索、执行函数、调用外部API。

## RAGs 检索增强生成
主要用于为大模型提供额外的信息源，提升回答问题的质量。但有一个问题是，直接将大量的私有文档输送给大模型，者往往受到模型上下文的限制。
