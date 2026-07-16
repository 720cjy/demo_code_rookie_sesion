import json
import os
from typing import Sequence
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from ollama import chat
import RAG_03_config_data as config



def get_history(session_id): #括号里的session_id 接收外部传入的值
    return FileChatMessageHistory(session_id, config.chat_history_path)

"""
FileChatMessageHistory = 文件型聊天记忆类（LangChain 内置）
两个入参：
session_id：以这个 id 命名本地存储文件，每个用户独立文件；
storage_path="./chat_history/"：聊天记录存放文件夹，所有用户对话文件都存在这个目录下。
"""

class FileChatMessageHistory(BaseChatMessageHistory):
    # 写在class（）里的是父类，子类 继承父类的所有方法和属性
    def __init__(self, session_id, storage_path):
        self.session_id = session_id        # 会话id
        self.storage_path = config.chat_history_path    # 不同会话id的存储文件，所在的文件夹路径
        # 完整的文件路径
        self.file_path = os.path.join(config.chat_history_path, self.session_id)
        # 确保文件夹是存在的
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        # Sequence序列 类似list、tuple
        all_messages = list(self.messages)      # 已有的消息列表
        all_messages.extend(messages)           # 新的和已有的融合成一个list

        # 将数据同步写入到本地文件中
        # 类对象写入文件 -> 一堆二进制
        # 为了方便，可以将BaseMessage消息转为字典（借助json模块以json字符串写入文件）
        # 官方message_to_dict：单个消息对象（BaseMessage类实例） -> 字典
        # new_messages = []
        # for message in all_messages:
        # d = message_to_dict(message)
        # new_messages.append(d)

        new_messages = [message_to_dict(message) for message in all_messages]
        # 将数据写入文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f)

    @property       # @property装饰器将messages方法变成成员属性用
    def messages(self) -> list[BaseMessage]:
        # 当前文件内： list[字典]
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)    # 返回值就是：list[字典]
                return messages_from_dict(messages_data)
        except FileNotFoundError:
            return []

    def clear(self) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)
