import os
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Event, MessageSegment
from pydub import AudioSegment
import subprocess

# 定义命令 'play_song'，别名为 '播放歌曲'
play_song = on_command("play_song", aliases={"播放歌曲"}, priority=5)

# 定义一个处理歌曲播放的命令
@play_song.handle()
async def handle_play_song(bot: Bot, event: Event):
    # 假设歌曲文件路径和名称
    song_path = "path/to/song.mp3"  # 你需要确保该路径存在且歌曲文件已经下载好
    
    # 将歌曲转换为 silk 格式
    silk_path = convert_to_silk(song_path)

    if silk_path:
        # 发送 silk 格式音频
        await bot.send(event, MessageSegment.record(file=f"file:///{silk_path}"))
    else:
        await bot.send(event, "歌曲播放失败，无法转换为 silk 格式。")

# 将 mp3 格式的文件转换为 silk 格式
def convert_to_silk(input_file):
    # 输出的 silk 文件路径
    output_file = input_file.replace(".mp3", ".silk")
    
    # 使用 pydub 将 mp3 文件转为 wav
    try:
        sound = AudioSegment.from_mp3(input_file)
        wav_file = input_file.replace(".mp3", ".wav")
        sound.export(wav_file, format="wav")

        # 使用 silk v3 encoder 将 wav 文件转换为 silk
        result = subprocess.run(["./silk_v3_encoder", wav_file, output_file, "-tencent"], capture_output=True)

        # 检查转换是否成功
        if result.returncode == 0:
            return output_file
        else:
            return None
    except Exception as e:
        print(f"转换失败: {e}")
        return None
