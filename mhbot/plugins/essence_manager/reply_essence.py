# 将被回复的消息设置为精华

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot_plugin_session import extract_session, SessionIdType

from .config import config
from ..tools.rules import has_reply


# 创建一个仅处理包含回复消息的处理器
essence_setter = on_command(
    cmd="j",
    aliases={"精", "精华消息", "设精", "设为精华", "精华"},
    rule=has_reply(),
    priority=config.essence_manual_priority,
    block=True,
)


@essence_setter.handle()
async def handle_reply(bot: Bot, event: MessageEvent):
    if not is_in_white_list(bot, event):
        return

    message_id = event.reply.message_id
    await bot.call_api("set_essence_msg", message_id=message_id)
    await essence_setter.send("吃我瞬发王八拳！")


essence_deleter = on_command(
    cmd="rm",
    aliases={"删除精华", "删除", "取消设精", "取消精华", "取消", "移出精华"},
    rule=has_reply(),
    priority=config.essence_manual_priority,
    block=True,
)


@essence_deleter.handle()
async def handle_delete(bot: Bot, event: MessageEvent):
    if not is_in_white_list(bot, event):
        return

    message_id = event.reply.message_id
    await bot.call_api("delete_essence_msg", message_id=message_id)
    await essence_deleter.send("金狮子撤回了一个王八拳。")


def is_in_white_list(bot: Bot, event: MessageEvent) -> bool:
    session = extract_session(bot, event)
    group_id = session.get_id(SessionIdType.GROUP).split("_")[-1]
    return group_id in config.essence_white_list
