import re
import json
import os
from nonebot import on_message, on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot_plugin_session import extract_session, SessionIdType

from .config import config

# 检测到疑似集会码时自动设精
auto_set_essence = on_message(priority=config.essence_auto_priority, block=True)

# 定义正则表达式，匹配形如 "=f7TXW!bCMa?" 的消息
pattern = re.compile(r"^[A-Za-z0-9!@#$%^&*()_+=?-]{12}$")
pattern2 = re.compile(r"^[A-Za-z0-9]{16}$")
# 排除AV号、BV号
sub_pattern = re.compile(r"^[AB]V[0-9a-zA-Z]{10}$")

JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "smdm.json")


@auto_set_essence.handle()
async def handle_message(bot: Bot, event: MessageEvent):
    session = extract_session(bot, event)
    group_id = session.get_id(SessionIdType.GROUP).split("_")[-1]
    if group_id not in config.essence_white_list:
        return

    message_content = event.get_plaintext().strip()  # 获取消息文本内容

    # 检查消息内容是否符合指定格式
    if pattern.match(message_content) or pattern2.match(message_content):
        if sub_pattern.match(message_content):
            return
        message_id = event.message_id  # 获取消息 ID

        # 调用 OneBot v11 API 设置精华
        try:
            await bot.call_api("set_essence_msg", message_id=message_id)
            await auto_set_essence.send("捕食到一条smdm！")

        except Exception as e:
            await auto_set_essence.send(f"设置精华消息失败: {e}")

        data = read_json(JSON_FILE_PATH)
        if pattern.match(message_content):
            id = data[group_id]["world"]
            try:
                await bot.call_api("delete_essence_msg", message_id=id)
                await auto_set_essence.send("已删除上一条smdm。")
            except Exception:
                pass
            data[group_id]["world"] = message_id
        else:
            id = data[group_id]["rise"]
            try:
                await bot.call_api("delete_essence_msg", message_id=id)
                await auto_set_essence.send("已删除上一条smdm。")
            except Exception:
                pass
            data[group_id]["rise"] = message_id

        write_json(data, JSON_FILE_PATH)


def read_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}


def write_json(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


# 一键删除精华中的smdm
clear_smdm = on_command(
    cmd="clear_smdm",
    aliases={"清除smdm", "clear", "c", "整理精华"},
    priority=config.essence_manual_priority,
    block=True,
)


@clear_smdm.handle()
async def handle_clear_smdm(bot: Bot, event: MessageEvent):
    session = extract_session(bot, event)
    group_id = session.get_id(SessionIdType.GROUP).split("_")[-1]
    if group_id not in config.essence_white_list:
        return

    essence_messages = await bot.call_api("get_essence_msg_list", group_id=group_id)
    for message in essence_messages:
        message_id = message["message_id"]
        mess = await bot.call_api("get_msg", message_id=message_id)
        if pattern.match(mess.get("raw_message", "")) or pattern2.match(
            mess.get("raw_message", "")
        ):
            await bot.call_api("delete_essence_msg", message_id=message_id)

    await clear_smdm.send("已删除所有smdm。")
