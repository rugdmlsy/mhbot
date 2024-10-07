from pydantic import BaseModel, Field
from nonebot import get_plugin_config


class Config(BaseModel):
    """Plugin Config Here"""

    essence_priority: int = (Field(1, doc="essence_manager 响应优先级"))
    essence_white_list: list = (Field([], doc="essence_manager 白名单"))


config = get_plugin_config(Config)