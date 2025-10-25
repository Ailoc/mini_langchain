from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_deepseek import ChatDeepSeek

load_dotenv()
model = ChatDeepSeek(model="deepseek-chat")

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个很聪明的ai助手！请以{tone}的语气，回答任何问题"),
    ("human", "{question}")
])

translate_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的翻译助手！请将以下中文内容翻译成英文："),
    ("human", "翻译以下的文章为{language}: {text}")
])

prepare_for_translation = RunnableLambda(lambda x: {"text": x, "language": "繁体中文"})

chain = prompt_template | model | StrOutputParser() | prepare_for_translation | translate_template | model | StrOutputParser()
result = chain.invoke({"tone": "幽默", "question": "讲述一下量子力学的基本原理。"})
print(result)