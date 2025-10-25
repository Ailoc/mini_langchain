import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from langchain_mongodb import MongoDBChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableConfig
from langchain_deepseek import ChatDeepSeek

# 加载环境变量
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")
COLLECTION_NAME = os.getenv("CONVERSATION_COLLECTION_NAME")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")  # 统一变量名
USER_ID = "user_123"  # 示例用户ID
SESSION_ID = f"{USER_ID}:session_1"  # 示例会话ID

def test_mongodb_connection():
    try:
        client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        print("Connected to MongoDB")
        client.close()
    except ConnectionFailure as e:
        raise ValueError("Could not connect to MongoDB")

def create_chatbot(session_id: str):
    test_mongodb_connection()

    llm = ChatDeepSeek(
        model="deepseek-chat",
        temperature=1.3,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个很聪明的ai助手！"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    chain = prompt | llm

    # get_session_history 函数：基于 session_id 返回 MongoDB 历史（1.0 签名）
    def get_session_history(session_id: str) -> MongoDBChatMessageHistory:
        return MongoDBChatMessageHistory(
            session_id=session_id,  # 必需（1.0 优先参数）
            connection_string=MONGODB_URI,
            database_name=DB_NAME,
            collection_name=COLLECTION_NAME
        )

    chain_with_history = RunnableWithMessageHistory(
        runnable=chain,
        get_session_history=get_session_history,  # 使用 get_session_history 参数名，并传递函数本身
        input_messages_key="input",
        history_messages_key="history"
    )
    return chain_with_history

if __name__ == "__main__":
    chatbot = create_chatbot(SESSION_ID)
    print("-------------Conversation started. Type 'exit' to end.-------------")

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() == "exit":
                break
            config = RunnableConfig(configurable={"session_id": SESSION_ID})
            response = chatbot.invoke(
                {"input": user_input},
                config=config
            )
            print("AI: ", response.content)
            client = MongoClient(MONGODB_URI)
            db = client[DB_NAME]
            db[COLLECTION_NAME].update_one(
                {"session_id": SESSION_ID},
                {"$set": {"user_id": USER_ID, "updated_at": datetime.utcnow()}},  # 使用 utcnow() 以 UTC 时间
                upsert=True
            )
            client.close()
        except KeyboardInterrupt:
            print("User interrupted")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

    print("-------------Conversation ended.-------------")