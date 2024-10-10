from nonebot.plugin import PluginMetadata

from .config import Config
from .music_player import play_song

__plugin_meta__ = PluginMetadata(
    name="audio_manager",
    description="",
    usage="",
    config=Config,
)
