from nonebot.plugin import PluginMetadata

from .config import Config
from .party_code import auto_set_essence

__plugin_meta__ = PluginMetadata(
    name="essence-manager",
    description="",
    usage="",
    config=Config,
)


