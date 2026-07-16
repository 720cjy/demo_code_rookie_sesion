# check md5 file exists
md5_path = "./RAG_project/data/md5.txt"

#chroma
collection_name = "RAG"
model ="text-embedding-v4"
persist_directory = "./RAG_project/data"

#splitter
chunk_overlap = 100
chunk_size = 1000
separator = ["\n\n","\n","。","，","！","？","！","？"]


#upload by str
max_splitter_char_number = 1000


#vector store
k = 2   #每次检索返回结果的数量


#rag
chat_history_path = "./RAG_project/chat_history.json"
embedding_model ="text-embedding-v4"
chat_model = "qwen3-max"

#RAG_07_app_pa
session_config = {
    "configurable": {
        "session_id": "user_001",
    }
}