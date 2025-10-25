from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableSequence
from langchain_deepseek import ChatDeepSeek

load_dotenv()
model = ChatDeepSeek(model="deepseek-chat")

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个很聪明的ai助手！请以{tone}的语气，回答任何问题"),
    ("human", "{question}")
])

format_template = RunnableLambda(lambda x: prompt_template.format(**x))
invoke_model = RunnableLambda(lambda x: model.invoke(x))
parse_output = RunnableLambda(lambda x: x.content)

# 将各个步骤组合成一个链,middle可以容纳多个runnable
chain = RunnableSequence(first=format_template, middle=[invoke_model], last=parse_output)
response = chain.invoke({"tone": "幽默", "question": "解释一下量子力学的基本原理。"})
print(response)