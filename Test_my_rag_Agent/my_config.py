from langchain_core.prompts import PromptTemplate
from langchain_community.chat_models import ChatTongyi

# 原有配置保留
DashScopeEmbedding_model = "text-embedding-v4"
collection_name = "my_knowledge"
persist_directory = "./chroma_test"

chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ",", "!", "?", ".", ":", ";", "，", "。"]

# 修正：实例化模型，不能只写字符串
chat_model = ChatTongyi(model="qwen-turbo")

k = 2
my_knowledge_path = "./data/knowledge.txt"


