from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

load_dotenv()
model = ChatDeepSeek(model="deepseek-chat")

summary_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个电影评论家"),
        ("human", "请你简要总结一下电影{movie_name}")
    ]
)

def analyze_plot(plot):
    plot_template = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个专注于电影情节分析的专家"),
            ("human", "请分析以下电影情节：{plot}, 其中有什么优点或者缺点")
        ]
    )
    return plot_template.format_prompt(plot=plot)

def analyze_characters(characters):
    character_template = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个专注于电影角色分析的专家"),
            ("human", "请分析以下电影角色：{characters}, 这些角色塑造得怎么样")
        ]
    )
    return character_template.format_prompt(characters=characters)

def combine_verdicts(plot_analysis, character_analysis):
    verdict_template = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个电影评论家"),
            ("human", "基于以下情节分析：{plot_analysis} 和角色分析：{character_analysis}，请给出你对这部电影的总体评价")
        ]
    )
    return verdict_template.format_prompt(plot_analysis=plot_analysis, character_analysis=character_analysis)

plot_branch_chain = (
    RunnableLambda(lambda inputs: analyze_plot(inputs)) | model | StrOutputParser()
)
character_branch_chain = (
    RunnableLambda(lambda inputs: analyze_characters(inputs)) | model | StrOutputParser()
)

chain = (
    summary_template
    | model
    | StrOutputParser()
    | RunnableParallel({"plot_branch": plot_branch_chain, "character_branch": character_branch_chain})
    | RunnableLambda(lambda x: combine_verdicts(x["plot_branch"], x["character_branch"]))
    | model
    | StrOutputParser()
)

result = chain.invoke({"movie_name": "让子弹飞"})
print(result)