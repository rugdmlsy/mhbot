from pydantic import BaseModel, Field
from nonebot import get_plugin_config


class Config(BaseModel):
    """Plugin Config Here"""

    essence_auto_priority: int = Field(10, doc="essence_manager 自动设精响应优先级")
    essence_manual_priority: int = Field(5, doc="essence_manager 手动设精响应优先级")
    essence_white_list: list = Field([], doc="essence_manager 白名单")
    essence_reply_keywords: list = Field(
        ["精华", "设精"], doc="essence_manager 回复关键词"
    )


config = get_plugin_config(Config)
