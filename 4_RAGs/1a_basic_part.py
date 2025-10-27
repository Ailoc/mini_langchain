import os
os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = '1'

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_milvus import Milvus

# import the Embeddings interface so our wrapper can satisfy the type expected by langchain
from langchain_huggingface import HuggingFaceEmbeddings

current_dir = os.path.dirname(os.path.realpath(__file__))
file_path = [os.path.join(current_dir, "documents", "huozhe.txt")]
documents = []
for book in file_path:
    loader = TextLoader(book)
    book_docs = loader.load()
    for doc in book_docs:
        doc.metadata = {"source": book}  # 为每个文档添加元数据，指明来源文件
        documents.append(doc)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100) # 每个文本块1000个字符，重叠100个字符，有助于保持上下文连续性
texts = text_splitter.split_documents(documents)

book_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Milvus.from_documents(
    documents=texts,
    embedding=book_embeddings,
    connection_args={"host": "localhost", "port": "19530"},
    collection_name="huozhe_collection"
)

print("Finished creating/adding documents to Milvus collection.")