from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_core.output_parsers import StrOutputParser  # 这个函数用于将输出解析为字符串，提取content属性

load_dotenv()
model = ChatDeepSeek(model="deepseek-chat")

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个很聪明的ai助手！请以{tone}的语气，回答任何问题"),
    ("human", "{question}")
])

chain = prompt_template | model | StrOutputParser()

result = chain.invoke({"tone": "幽默", "question": "解释一下量子力学的基本原理。"})
print(result)