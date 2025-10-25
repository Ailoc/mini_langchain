from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch
from langchain_deepseek import ChatDeepSeek

load_dotenv()
model = ChatDeepSeek(model="deepseek-chat")

classification_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个高情商的智能客服助理"),
        ("human", "请你根据以下反馈，判断这条反馈是正面的、负面的，还是中立的：{feedback}"),
    ]
)

positive_feedback_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个积极乐观的客服助理"),
    ("human", "这是一条正面反馈：{feedback}。请你回复感谢客户的支持，并表达我们会继续努力提供更好的服务。回复包含太阳表情")
])
negative_feedback_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个有同理心的客服助理"),
    ("human", "这是一条负面反馈：{feedback}。请你回复道歉，并表示我们会认真对待客户的意见，努力改进服务。回复包含雨云表情")
])
neutral_feedback_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个中立客观的客服助理"),
    ("human", "这是一条中立反馈：{feedback}。请你回复感谢客户的反馈，并表示我们会继续关注客户的需求。回复包含微笑表情")
])

branches = RunnableBranch(
    (
        lambda x: "正面" in x,
        positive_feedback_template | model | StrOutputParser()
    ),
    (
        lambda x: "负面" in x,
        negative_feedback_template | model | StrOutputParser()
    ),
    neutral_feedback_template | model | StrOutputParser()
)

classification_chain = classification_template | model | StrOutputParser()

chain = classification_chain | branches
feedback = "我对你们的服务感到非常失望，又非常好，很不错，太垃圾了"
result = chain.invoke({"feedback": feedback})
print(result)