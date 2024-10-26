from nonebot.plugin import PluginMetadata

from .config import Config
from .party_code import auto_set_essence, clear_smdm
from .reply_essence import essence_setter, essence_deleter

__plugin_meta__ = PluginMetadata(
    name="essence-manager",
    description="",
    usage="",
    config=Config,
)
