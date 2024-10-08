# 将被回复的消息设置为精华

from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message
from nonebot.rule import Rule

from .config import config

# 规则1：检查消息是否包含回复
def has_reply() -> Rule:
    async def _has_reply(bot: Bot, event: MessageEvent) -> bool:
        # 检查消息中是否包含 reply 字段
        return event.get_message().get("reply") is not None
    return Rule(_has_reply)

# 规则2：检查消息是否包含指定的关键词
def contains_keyword(keywords: list) -> Rule:
    async def _contains_keyword(bot: Bot, event: MessageEvent) -> bool:
        message_content = event.get_plaintext().strip()
        return any(keyword in message_content for keyword in keywords)
    return Rule(_contains_keyword)

keywords = config.essence_reply_keywords

# 创建一个仅处理包含回复消息的处理器
reply_handler = on_message(rule=has_reply() & contains_keyword(keywords), priority=config.essence_priority, block=False)

@reply_handler.handle()
async def handle_reply(bot: Bot, event: MessageEvent):
    message_id = event.reply.message_id
    # await reply_handler.send(f"检测到回复 {event.reply}，原始消息 ID 为 {message_id }")
    await bot.call_api("set_essence_msg", message_id=message_id )
    await reply_handler.send(f"吃我瞬发王八拳！")

