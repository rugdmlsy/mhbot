from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, Event
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from pydub import AudioSegment
import os
import random
import json

from .config import config

play_song = on_command(
    "play", aliases={"播放"}, priority=config.audio_priority, block=True
)
json_file_path = os.path.join(os.path.dirname(__file__), "audio_dict.json")
songs_folder = os.path.join(os.path.dirname(__file__), r"..\..\..\assets\songs")
# songs_folder = r"C:\Users\xyc\Documents\Projects\QQBot\mhbot\assets\songs"


# 读取JSON文件
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return None


# 查找字典中key对应的value
def find_value_in_json(file_path, key):
    data = load_json(file_path)
    if data:
        return data.get(key, "None")
    return None


# 从文件夹中随机选择一个文件
def select_random_file(folder_path):
    files = []

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            relative_path = os.path.relpath(os.path.join(dirpath, f), folder_path)
            files.append(relative_path)

    # 检查是否有文件可供选择
    if not files:
        return None

    random_file = random.choice(files)

    return os.path.join(folder_path, random_file), random_file


# 随机截取音频的15秒片段
def get_random_audio_clip(file_path, duration=15):
    audio = AudioSegment.from_file(file_path)
    audio_length = len(audio)

    if audio_length <= duration * 1000:
        return audio

    start_point = random.randint(0, audio_length - duration * 1000)
    end_point = start_point + duration * 1000

    return audio[start_point:end_point]


# 将音频片段保存到一个临时文件
def save_temp_audio_clip(audio_clip, output_path):
    audio_clip.export(output_path, format="mp3")


# 定义一个处理歌曲播放的命令
@play_song.handle()
async def handle_play_song(matcher: Matcher, args: Message = CommandArg()):
    args = args.extract_plain_text().strip()

    # 随机点歌
    if not args or args == "random" or args == "随机" or args == "mygo":
        song_path, song = select_random_file(songs_folder)
        await matcher.send(MessageSegment.record(file=song_path))
        await matcher.send(MessageSegment.text(f"正在播放：{song}"))
        return

    # 随机播放片段
    elif args == "clip":
        song_path, song = select_random_file(songs_folder)
        audio_clip = get_random_audio_clip(song_path)
        temp_audio_path = os.path.join(os.path.dirname(__file__), "temp_audio_clip.mp3")
        save_temp_audio_clip(audio_clip, temp_audio_path)
        await matcher.send(MessageSegment.record(file=temp_audio_path))
        await matcher.send(MessageSegment.text(f"正在播放随机片段：{song}"))
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        return

    # 播放指定歌曲
    else:
        # 从json文件中查找歌曲
        song_path = find_value_in_json(json_file_path, args)
        # song_path = os.path.join(songs_folder, f"{args}")
        # if not song_path.endswith(".mp3"):
        #     song_path += ".mp3"
        song_path = os.path.join(songs_folder, song_path)
        if not os.path.exists(song_path):
            await matcher.send(MessageSegment.text(f"找不到歌曲：{args}"))
            return
        await matcher.send(MessageSegment.record(file=song_path))
        await matcher.send(MessageSegment.text(f"正在播放：{args}"))
