from pydantic import BaseModel
from nonebot import get_plugin_config
from pydantic import Field


class Config(BaseModel):
    """Plugin Config Here"""

    chat_priority: int = Field(10, description="ai_chat 响应优先级")
    chat_app_id: str = Field(..., description="ai_chat app_id")
    chat_secret_key: str = Field(..., description="ai_chat secret_key")
    chat_access_token: str = Field(..., description="ai_chat access_token")


config = get_plugin_config(Config)
