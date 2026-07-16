import os.path
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
load_dotenv()
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
import my_config as mc
from langchain_text_splitters import RecursiveCharacterTextSplitter

rag_prompt  = ChatPromptTemplate.from_messages([
            ("system","根据资料回答问题，资料：{context},问题：{question}")
        ])

class VectorStore:
    def __init__(self):
        self.chroma = Chroma(
            collection_name=mc.collection_name,
            embedding_function=DashScopeEmbeddings(model = mc.DashScopeEmbedding_model),
            persist_directory=mc.persist_directory,
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=mc.chunk_size,
            chunk_overlap =mc.chunk_overlap,
            separators=mc.separators,
        )
    def add_text(self):
        file_path = mc.my_knowledge_path
        if not os.path.exists(file_path):
            return f"【失败】向量库不存在"
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            spliter_docs = self.spliter.split_text(text)
            self.chroma.add_texts(spliter_docs)
            return f"【成功】已存入向量库"
    def get_retriever(self):
        return self.chroma.as_retriever(search_kwargs={"k":mc.k})


