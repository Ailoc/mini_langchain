from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import datetime
from langchain_core.tools import tool
from langchain.agents import create_agent
from pydantic import BaseModel,Field
from typing import List
load_dotenv()
model = ChatOpenAI(model="ep-m-20250905173140-5fh2w")

@tool
def getNowTime():
    '''获取当前时间的工具函数'''
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"{current_time}"

query = "请告诉我现在的时间,并在未来的两个小时的时间给我安排一个学习计划。至少三个任务，每个任务持续30分钟到1小时之间。"

class Task(BaseModel):
    TimeChunk: str = Field(..., description="时间段，如 '22:08-23:08'")
    StudyPlan: str = Field(..., description="学习任务描述，30min-1h")

class TimeList(BaseModel):
    Todo: List[Task] = Field(..., description="至少3个任务的列表")

tools = [getNowTime]

system_prompt = """你是一个智慧助手, 可以帮助人们利用工具解决很多问题。
重要规则：
- 对于查询，先检查是否需要工具。如果需要，只调用一次相关工具获取信息。
- 获取信息后，立即基于它生成 Final Answer（最终响应），不要进一步调用工具。
- Final Answer 格式：直接回复用户，包括时间和学习计划（e.g., 根据时间段建议 1-2 小时学习任务）。
- 避免重复调用工具。"""

agent = create_agent(model, system_prompt=system_prompt, tools=tools, response_format=TimeList)
# response = agent.invoke({"messages": [{"role": "user", "content": query}]})
# for i, message in enumerate(response["messages"]):
#     message.pretty_print()

# 使用streaming模式
for token, metadata in agent.stream({"messages": [{"role": "user", "content": query}]}, stream_mode="messages"):
    print(f"{token.content}", end="")
