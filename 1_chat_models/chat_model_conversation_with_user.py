from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()
chat_history = []
llm = ChatOpenAI(model="ep-m-20250905173140-5fh2w", streaming=True)
systemMessage = SystemMessage(content="你是一个很聪明的ai助手！")
chat_history.append(systemMessage)

while True:
    query = input("User: ")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))
    # 流式输出：收集完整响应并实时打印
    full_response = ""
    print("AI: ", end="", flush=True)  # 开始打印 AI 响应，无换行
    for chunk in llm.stream(chat_history):
        if chunk.content:  # 确保 chunk 有内容
            print(chunk.content, end="", flush=True)  # 流式打印每个 token/chunk
            full_response += chunk.content
    print()  # 结束响应后换行

    # 将完整响应追加到历史记录中
    chat_history.append(AIMessage(content=full_response))

print("-------------Conversation ended.-------------")
print(chat_history)