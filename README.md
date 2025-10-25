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

🧠 七、辅助组件（次核心）

| 模块                  | 功能                                                         |
| ------------------- | ---------------------------------------------------------- |
| **Retrievers**      | 从文档中检索上下文（RAG）                                             |
| **VectorStores**    | 文档向量数据库（如 FAISS、Chroma、Milvus、MongoDB Atlas Vector Search） |
| **DocumentLoaders** | 加载 PDF、TXT、网页等文档                                           |
| **TextSplitters**   | 文本分块（RAG 前处理）                                              |
| **OutputParsers**   | 解析模型输出为结构化数据                                               |
