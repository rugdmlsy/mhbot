from nonebot import on_message
from nonebot.adapters.onebot.v11 import MessageEvent, Event
from nonebot.rule import to_me, Rule
import requests

from .config import config

APP_ID = config.chat_app_id
SECRET_KEY = config.chat_secret_key
ACCESS_TOKEN = config.chat_access_token


# 调用文心对话 API
def call_wenxin_conversation(user_message, user_id):
    url = f"https://agentapi.baidu.com/assistant/getAnswer?appId={APP_ID}&secretKey={SECRET_KEY}"

    headers = {"Content-Type": "application/json"}
    data = {
        "message": {"content": {"type": "text", "value": {"showText": user_message}}},
        "source": APP_ID,
        "from": "openapi",
        "openId": user_id,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.json().get("status", "Not found") == 0:
        return (
            response.json()
            .get("data", {})
            .get("content", [])[0]
            .get("data", "未知错误")
        )
    else:
        return response.json().get("status", "Not found")


# 捕捉@机器人的消息
ai_chat_matcher = on_message(rule=to_me(), priority=config.chat_priority, block=True)


@ai_chat_matcher.handle()
async def handle_at_message(event: Event):
    user_message = str(event.get_plaintext().strip())
    if user_message == "":
        return
    if user_message.startswith("处理时出错:"):
        user_message = "猿神正在睡觉，不想理你。"
    user_id = event.get_user_id()
    if user_message:
        try:
            reply = call_wenxin_conversation(user_message, user_id)
        except Exception as e:
            reply = f"处理时出错: {str(e)}"

        # 发送回复
        await ai_chat_matcher.send(reply)
