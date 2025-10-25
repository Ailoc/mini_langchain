from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
llm = ChatDeepSeek(model="deepseek-chat")

template = "你是一个很聪明的ai助手！请以{tone}的语气，回答任何问题"

prompt_template = ChatPromptTemplate.from_template(template)
# 以下的invoke用于替换占位符
prompt = prompt_template.invoke(
    {
        "tone": "幽默"
    }
)
response = llm.invoke(prompt)
print(response.content)