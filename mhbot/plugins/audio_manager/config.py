from pydantic import BaseModel, Field
from nonebot import get_plugin_config


class Config(BaseModel):
    """Plugin Config Here"""

    audio_priority: int = Field(5, description="audio_manager 响应优先级")


config = get_plugin_config(Config)
