from vector_store import VectorStore,rag_prompt
from langchain_core.prompts import ChatPromptTemplate
import os
import my_config as mc
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def print_prompt(prompt):
    print("*"*50)
    print(prompt)
    print("*"*50)
    return prompt

class RagService:
    def __init__(self):
        self.vector_store = VectorStore()
        self.prompt = rag_prompt
        self.chat_model = mc.chat_model
        self.parser = StrOutputParser()

    def answer(self,question):
        chain = (({"question":RunnablePassthrough(),
                   "context":self.vector_store.get_retriever()})
                 | self.prompt
                 | print_prompt
                 | self.chat_model
                 | self.parser )
        return chain.invoke(question)


if __name__ == "__main__":
    VS = VectorStore()
    VS.add_text()
    rag_service = RagService()
    print(rag_service.answer("放置有什么要求"))
