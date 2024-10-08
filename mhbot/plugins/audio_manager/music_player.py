from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, Event
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from pydub import AudioSegment
import os
import random

play_song = on_command("play", aliases={"播放"}, priority=5)


# 从文件夹中随机选择一个文件
def select_random_file(folder_path):
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

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


songs_folder = os.path.join(os.path.dirname(__file__), r"..\..\..\assets\songs\MyGO")


# 定义一个处理歌曲播放的命令
@play_song.handle()
async def handle_play_song(matcher: Matcher, args: Message = CommandArg()):
    args = args.extract_plain_text().strip()

    if not args or args == "random" or args == "随机" or args == "mygo":
        song_path, song = select_random_file(songs_folder)
        await matcher.send(MessageSegment.record(file=song_path))
        await matcher.send(MessageSegment.text(f"正在播放：{song}"))
        return

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

    else:
        song_path = os.path.join(songs_folder, f"{args}")
        if not song_path.endswith(".mp3"):
            song_path += ".mp3"
        if not os.path.exists(song_path):
            await matcher.send(MessageSegment.text(f"找不到歌曲：{args}"))
            return
        await matcher.send(MessageSegment.record(file=song_path))
        await matcher.send(MessageSegment.text(f"正在播放：{args}"))
