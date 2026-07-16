import hashlib
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
load_dotenv()
import RAG_03_config_data


def check_md5(md5_str: str):
    if not os.path.exists(RAG_03_config_data.md5_path):
        open(RAG_03_config_data.md5_path, 'w', encoding="utf-8").close()
        return False
    else:
        for line in open(RAG_03_config_data.md5_path, 'r', encoding="utf-8").readlines():
            line = line.strip()
            if line == md5_str:
                return True
        return False

def save_md5(md5_str: str):
    with open(RAG_03_config_data.md5_path, 'a', encoding="utf-8") as f:
        f.write(md5_str + "\n")

def get_string_md5(input_str: str, encoding="utf-8"): # 将传入字符串转换为md5字符串
    str_bytes = input_str.encode(encoding=encoding) # 将字符串转换为字节
    md5_obj = hashlib.md5()         # 得到md5对象，可以理解为一个计算器
    md5_obj.update(str_bytes)       # 更新内容
    md5_hex = md5_obj.hexdigest()   # 转换成十六进制字符串
    return md5_hex

class KnowledgeBaseService(object):
    # 作用是创建 / 加载本地持久化的Chroma向量库，搭配阿里通义 DashScope 向量化模型，用来存文档向量。
    def __init__(self):
        os.makedirs(RAG_03_config_data.persist_directory, exist_ok=True)  # 如果文件夹不存在则创建，存在则跳过
        # Chroma 是轻量级本地向量数据库，专门用来存储文档的向量，做相似度检索
        self.chroma = Chroma(
            collection_name=RAG_03_config_data.collection_name,  # 数据库的表名
            embedding_function=DashScopeEmbeddings(model=RAG_03_config_data.model),  # 向量化模型
            persist_directory=RAG_03_config_data.persist_directory,  # 数据库的存储路径
        )
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=RAG_03_config_data.chunk_size,  # 分割后文本最大长度
            chunk_overlap=RAG_03_config_data.chunk_overlap,  # 连续文本段之间的字符重叠数量
            separators=RAG_03_config_data.separator,  # 自然段落划分的符号（这里还有拼写坑后面说）
            length_function=len,  # 计算文本长度的函数
        )
    def upload_by_str(self, data:str, filename):
    # 将传入字符串，进行向量化，存入向量数据库中
    # 先得到字符串的md5值
        md5_str = get_string_md5(data)
    # 检查md5值是否已存在
        if check_md5(md5_str): # 默认是True表明处理过则print
            return "已存在，跳过"

        if len(data) > RAG_03_config_data.max_splitter_char_number:
            knowledge_chunks :list[str]= self.splitter.split_text(data)
        else:
            knowledge_chunks = [data]
        metadata={
            "source" : filename,
            "create_time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator" : "小菜"
        }
        self.chroma.add_texts(
            knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks] #[ 每次循环要放进列表的值  for 变量 in 循环对象 ]
                # 最前面的 metadata = 【每一轮循环，往新列表里放什么内容】
            )   # 每次循环，往列表里放入同一个metadata字典。
                # 这个循环里我不需要取出 chunk 的内容，我只是借用它来统计【循环次数】。
                # 我只关心：一共有多少个文本分片，就要生成多少个 metadata。
        save_md5(md5_str)
        return "向量库已经记录"

if __name__ == '__main__':
    service = KnowledgeBaseService()
    r1 =service.upload_by_str("你好", "test.txt")
    print(r1)
