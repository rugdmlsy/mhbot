from pydantic import BaseModel
from nonebot import get_plugin_config
from pydantic import Field


class Config(BaseModel):
    """Plugin Config Here"""

    sender_priority: int = Field(5, doc="sender 响应优先级")
    sender_to_groups: list = Field([], doc="sender 发送目标群组")


config = get_plugin_config(Config)
