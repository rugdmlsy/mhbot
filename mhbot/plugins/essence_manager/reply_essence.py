# 将被回复的消息设置为精华
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot_plugin_session import extract_session, SessionIdType

from .config import config

# 创建一个消息处理器，监听所有群消息
reply_essence = on_message(priority=config.essence_priority, block=False)


@reply_essence.handle()
async def handle_message(bot: Bot, event: MessageEvent):

    session = extract_session(bot, event)
    group_id = session.get_id(SessionIdType.GROUP).split("_")[-1]
    if group_id not in config.essence_white_list:
        return
    
    message_content = event.get_plaintext().strip()  # 获取消息文本内容

    # 检查消息内容是否符合指定格式
    if pattern.match(message_content):
        if sub_pattern.match(message_content):
            return
        message_id = event.message_id  # 获取消息 ID

        # 调用 OneBot v11 API 设置精华
        try:
            await bot.call_api("set_essence_msg", message_id=message_id)
            await auto_set_essence.send("捕食到一条smdm！")
        except Exception as e:
            await auto_set_essence.send(f"设置精华消息失败: {e}")

