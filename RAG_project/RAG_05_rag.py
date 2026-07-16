from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory, RunnableLambda
from langchain_core.documents import Document
import RAG_03_config_data
from RAG_06_history_dialog_store import get_history
from RAG_04_vector_store import VectorStore
load_dotenv()

def print_prompt(prompt):
    print("=" * 20)
    print(prompt.to_string())
    print("=" * 20)
    return prompt

class RagService(object):
    def __init__(self):
        self.vector_service = VectorStore(
            embedding_model=DashScopeEmbeddings(model=RAG_03_config_data.embedding_model),
        )
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "以我提供的资料为主，简洁回答用户问题，参考资料：{context}"),
            ("system","并且提供用户的对话历史记录，如下{history}"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "请回答用户提问{input}")
        ])
        self.chat_model = ChatTongyi(model=RAG_03_config_data.chat_model)
        self.chain = self.__get_chain()

    def __get_chain(self):  # 获取最终执行链
        retriever = self.vector_service.get_retriever()

        def format_document(docs: list[Document]): # 检索到的文档格式化
            if not docs:
                return "无相关资料"

            formatted_str = ""
            for doc in docs:
                source = doc.metadata.get("source", "未知文档")
                # 从字典里找叫source的信息，如果找不到这个 key，就默认返回「未知文档」。
                # page_content：文档的正文纯文字（真正的资料内容）。
                # metadata：文档的元数据（就是备注信息，存在一个字典里，比如文件名、来源、页码、创建时间这些）。
                formatted_str += f"文档来源：{source}\n文档内容：{doc.page_content}\n\n"
            return formatted_str
             #作用是给检索器准备检索关键词

        def format_for_retriever(value: dict) -> str:  #-> str这个函数执行完，返回的数据类型一定是str类型
            return value["input"]

        def format_for_prompt_template(value):
            # {input, context, history}  拆包重组
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["context"] = value["context"]
            new_value["history"] = value["input"]["history"]
            return new_value

        chain = (
                {
                    "input": RunnablePassthrough(),  # 保留原始数据的
                    "context": RunnableLambda(format_for_retriever)
                #｜是 LangChain 专属的流水线连接符，只能连接「Runnable 类型」的对象
                | retriever
                | format_document
                }
                | RunnableLambda(format_for_prompt_template)
                | self.prompt_template
                | print_prompt
                | self.chat_model
                | StrOutputParser()
        )
        # RunnableWithMessageHistory带消息历史的可运行包装器
        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        return conversation_chain

if __name__ == '__main__':
    # session id 配置
    session_config = {
        "configurable": {
            "session_id": "user_001",
        }
    }
    service = RagService()
    res = service.chain.invoke({"input": "我身高160，需要买什么尺码"}, session_config)
    print(res)