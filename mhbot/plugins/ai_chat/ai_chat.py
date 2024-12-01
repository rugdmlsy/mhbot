import random
import os

from nonebot import on_message
from nonebot.adapters.onebot.v11 import MessageEvent, Event, MessageSegment
from nonebot.rule import to_me, Rule
import requests

from .config import config

APP_ID = config.chat_app_id
SECRET_KEY = config.chat_secret_key
ACCESS_TOKEN = config.chat_access_token
ID_OFFSET = ""

# 读取ID_OFFSET
current_dir = os.path.dirname(os.path.abspath(__file__))  # 当前脚本的绝对路径
id_offset_file_path = os.path.join(current_dir, "id_offset.txt")
with open(id_offset_file_path, "r", encoding="utf-8") as file:
    ID_OFFSET = file.read().strip()


# 调用文心对话 API
def call_wenxin_conversation(user_message, user_id):
    url = f"https://agentapi.baidu.com/assistant/getAnswer?appId={APP_ID}&secretKey={SECRET_KEY}"

    headers = {"Content-Type": "application/json"}
    data = {
        "threadId": user_id + ID_OFFSET,
        "message": {
            "content": {"type": "text", "value": {"showText": user_message}},
        },
        "source": APP_ID,
        "from": "openapi",
        "openId": user_id,
    }
    response = requests.post(url, headers=headers, json=data)
    json_data = response.json()
    if response.json().get("status", "Not found") == 0:
        answer = json_data.get("data", {}).get("content", [])[0].get("data", "未知错误")
        if answer == "您的问题我还不知道，麻烦换个问题试试~":
            with open(id_offset_file_path, "w", encoding="utf-8") as file:
                file.write(str(random.randint(10**9, 10**10 - 1)))
        return answer
    else:
        return str(json_data.get("status", "Not found")) + json_data.get(
            "message", "Not found"
        )


# 捕捉@机器人的消息
# ai_chat_matcher = on_message(rule=to_me(), priority=config.chat_priority, block=True)


# @ai_chat_matcher.handle()
# async def handle_at_message(event: Event):
#     user_message = str(event.get_plaintext().strip())
#     if user_message == "":
#         return
#     user_id = event.get_user_id()
#     # if user_message:
#     #     try:
#     #         reply = call_wenxin_conversation(user_message, user_id)
#     #     except Exception as e:
#     #         reply = f"处理时出错: {str(e)}"

#     # if reply.startswith("处理时出错:"):
#     #     reply = "猿神正在睡觉，不想理你。"
#     # # 发送回复
#     await ai_chat_matcher.send(MessageSegment.at(user_id) + "我草饲你")
