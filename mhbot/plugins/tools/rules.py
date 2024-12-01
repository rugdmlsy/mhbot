from typing import Pattern

from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

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


def send_by_superusers() -> Rule:
    async def _send_by_superuser(bot: Bot, event: MessageEvent) -> bool:
        return event.get_user_id() in config.superusers

    return Rule(_send_by_superuser)


def match_regex(*args: Pattern) -> Rule:
    async def _match_regex(bot: Bot, event: MessageEvent) -> bool:
        message_content = event.get_plaintext().strip()
        ret = False
        for regex in args:
            ret = ret or regex.match(message_content)
        return ret

    return Rule(_match_regex)
