from langchain_chroma import Chroma
from dotenv import load_dotenv
import RAG_03_config_data as config
load_dotenv()

class VectorStore:
    def __init__(self,embedding_model): #嵌入模型  文本转向量需要嵌入模型
        self.embedding_model = embedding_model
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding_model,
            persist_directory=config.persist_directory,
        )
    def get_retriever(self):   #返回向量检索器，方便加入chain。
         #可以理解成retriever是一个搜索器，搜索最相关的片段
         return self.vector_store.as_retriever(search_kwargs={"k": config.k})

if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    retriever = VectorStore(DashScopeEmbeddings(model = "text-embedding-v4")).get_retriever()
    print(retriever.invoke("你好"))
"""
从 Chroma 向量库中创建检索器（Retriever），专门做相似度检索：
接收用户提问；
把问题向量化；
在向量库里匹配最相似的文本片段；
返回匹配到的原文，交给 LLM 做上下文回答。
"""