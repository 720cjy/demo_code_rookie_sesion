from langchain_chroma import Chroma
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
import my_config as mc
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
from dotenv import load_dotenv
load_dotenv()

DashScopeEmbeddings_model = DashScopeEmbeddings(model=mc.DashScopeEmbedding_model)
text_chroma = Chroma(
    collection_name=mc.collection_name,
    embedding_function=DashScopeEmbeddings_model,
    persist_directory=mc.persist_directory
)
text_spliter =RecursiveCharacterTextSplitter(
    chunk_size=mc.chunk_size,
    chunk_overlap =mc.chunk_overlap,
    separators=mc.separators,
)
chat_model = ChatTongyi(model=mc.chat_model)

prompt = ChatPromptTemplate.from_messages([
    ("system","根据资料回答问题，资料：{context},问题：{question}")
])

def print_prompt(prompt):
    print("-"*30)
    print(prompt)
    print("-"*30)
    return prompt

def upload_knowledge():
    """读取知识库文件 → 分块 → 存入向量库 → 持久化"""
    file_path = mc.my_knowledge_path
    if not os.path.exists(file_path):
        return f"【失败】知识库文件不存在：{file_path}"
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    split_docs = text_spliter.split_text(text)  # 输入字符串，输出字符串列表
    text_chroma.add_texts(split_docs)           # 专门接收字符串列表
    return f"【成功】已存入向量库，共 {len(split_docs)} 个文本块"

def get_retriever():
    return text_chroma.as_retriever(search_kwargs = {"k": mc.k})

def _chain():
    chain = (({"question":RunnablePassthrough(),"context":get_retriever()})
         | prompt | print_prompt |chat_model | StrOutputParser())
    return chain

if __name__ == "__main__":
    upload_knowledge()
    chain = _chain()
    res = chain.invoke("你有什么核心技术")
    print(res)
