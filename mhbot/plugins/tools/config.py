from pydantic import BaseModel
from nonebot import get_plugin_config
from pydantic import Field


class Config(BaseModel):
    """Plugin Config Here"""

    superusers: list = Field([], doc="超级用户列表")


config = get_plugin_config(Config)
