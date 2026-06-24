

import os
from openai import OpenAI, api_key
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("DEEPSEEK_API_KEY")
client =OpenAI(api_key = api_key,base_url = "https://api.deepseek.com")

print("==欢迎来到cjy channel，有问题可以提出（按'q'退出)==")
message = []
message.append({"role":"system","content":"你是一个温柔的助手"})
while True:
    ask = input("请输入你的问题\n")
    if ask.lower() == 'q':
        print("程序退出了")
        break
    message.append({"role": "user", "content": ask})
    try:
        answer = client.chat.completions.create(
            model = "deepseek-chat",
            messages = message,
            temperature = 0.8,
            timeout = 10,
            stream = True
        )

        ai_answer = ""
        for x in answer:
            content = x.choices[0].delta.content
            if content:
                ai_answer += content
                print(content, end='', flush=True)
        print()
        message.append({"role": "assistant", "content": ai_answer})
    except Exception as e:
        print(f"出错了{e}")









import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("DEEPSEEK_API_KEY")

client = OpenAI (api_key = api_key,base_url="https://api.deepseek.com")
print("===欢迎来到深度求索（按'q'退出）===")
message = []
message.append({"role":"system","content":"你是一个正式的助手"})
while True:
    ask = input("输入你的问题\n")
    if ask.lower()== 'q':
        print("程序结束了")
        break
    message.append({"role": "user", "content": ask})
    try:
        answer = client.chat.completions.create(
            model = "deepseek-chat",
            timeout = 20,
            messages = message,
            stream = False
        )
        ai_answer = answer.choices[0].message.content
        print(ai_answer)
        message.append({"role":"assistant","content":ai_answer})
    except Exception as e:
        print(f"出错了{e}")
