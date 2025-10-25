from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

messages = [
    SystemMessage("你是一个助眠故事撰写专家！"),
    # HumanMessage("请给我讲一个关于勇敢小兔子的睡前故事。"),
]

load_dotenv()
chat_history = []
llm = ChatOpenAI(model="doubao-seed-1-6-flash-250715")
systemMessage = SystemMessage(content="你是一个很聪明的ai助手！")
chat_history.append(systemMessage)

while True:
    query = input("User: ")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))
    result = llm.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))
    print("AI: ", response)

print("-------------Conversation ended.-------------")
print(chat_history)