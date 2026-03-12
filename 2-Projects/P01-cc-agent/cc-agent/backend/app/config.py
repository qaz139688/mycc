from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
import json
import os

class Settings(BaseSettings):
    model_config = ConfigDict(
        protected_namespaces=(),
        env_prefix="AI_AGENT_"
    )
    
    api_key: str = ""
    api_base_url: str = "https://api.openai.com/v1"
    model_name: str = "gpt-4"
    telegram_token: str = ""
    telegram_chat_id: str = ""
    metaso_api_key: str = ""
    user_custom_prompt: str = ""
    user_preferences: str = ""
    personality_file: str = ""
    personality_content: str = ""
    feishu_app_id: str = ""
    feishu_app_secret: str = ""
    feishu_encrypt_key: str = ""
    feishu_verification_token: str = ""
    feishu_chat_id: str = ""
    acp_enabled: bool = False
    acp_data_path: str = ""
    acp_seed_password: str = "123456"
    acp_access_point: str = "agentid.pub"
    acp_agent_name: str = ""
    acp_aid: str = ""
    acp_debug: bool = False

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "config.json")

def ensure_data_dir():
    data_dir = os.path.dirname(CONFIG_FILE)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

def load_settings() -> Settings:
    ensure_data_dir()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return Settings(**data)
        except Exception:
            pass
    return Settings()

def save_settings(settings: Settings) -> None:
    ensure_data_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(settings.model_dump(), f, indent=2, ensure_ascii=False)
