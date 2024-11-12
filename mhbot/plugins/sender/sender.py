from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Bot, Message
from nonebot.params import CommandArg

from .config import config
from ..tools.rules import send_by_superusers

silk_sender = on_command(
    cmd="say",
    aliases={"speak", "说", "audio", "silk"},
    rule=send_by_superusers(),
    priority=config.sender_priority,
    block=True,
)


@silk_sender.handle()
async def handle_silk(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    arg = arg.extract_plain_text().strip().split()
    file = arg[0]
    for group_id in config.sender_to_groups:
        await silk_sender.send(MessageSegment.record(file), group_id=group_id)
