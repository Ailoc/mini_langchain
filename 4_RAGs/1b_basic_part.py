from langchain_milvus import Milvus
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_deepseek import ChatDeepSeek
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore_loaded = Milvus(
    embeddings,
    connection_args={"host": "localhost", "port": "19530"},
    collection_name="huozhe_collection",
)

query = "富贵的结局是怎样的？"
retriever = vectorstore_loaded.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 10, "score_threshold": 0.3}  # 检索最相似的10个文档，默认L2距离，越小越相似
)

docs = retriever.invoke(query)

combine_input = (
    "这儿有一些文件可以帮助你回答以下问题: "
    + query
    + "\n相关的文档为: \n"
    + "\n".join([doc.page_content for doc in docs])
    + "\n请基于以上内容，简要回答问题。"
)

model = ChatDeepSeek(model="deepseek-chat")
message = [
    SystemMessage(content="你是一个文章分析助手，擅长从文章中内容中进行分析。"),
    HumanMessage(content=combine_input)
]

chain = model | StrOutputParser()
result = chain.invoke(message)
print(result)