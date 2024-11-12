from nonebot.plugin import PluginMetadata

from .sender import silk_sender

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="sender",
    description="",
    usage="",
    config=Config,
)
