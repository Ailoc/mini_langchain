from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

load_dotenv()
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=1.3,
)

result = llm.invoke("Hello, DeepSeek!")
print(result.content)

