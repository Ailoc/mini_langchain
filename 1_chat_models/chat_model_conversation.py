from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

messages = [
    SystemMessage("你是一个助眠故事撰写专家！"),
    HumanMessage("请给我讲一个关于勇敢小兔子的睡前故事。"),
]

load_dotenv()
# llm = ChatDeepSeek(
#     model="deepseek-chat",
#     temperature=1.3,
# )
#
# result = llm.invoke(messages)
# print(result.content)

llm = ChatOpenAI(model="doubao-seed-1-6-flash-250715")
result = llm.invoke(messages)
print(result.content)