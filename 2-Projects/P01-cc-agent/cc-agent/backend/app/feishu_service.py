import httpx
import logging
import json
from typing import Optional, Dict, Any

from app.config import load_settings
from app.feishu_bot import feishu_bot

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_feishu_message(message: str, receive_id: Optional[str] = None) -> dict:
    settings = load_settings()
    
    app_id = settings.feishu_app_id
    app_secret = settings.feishu_app_secret
    chat_id = receive_id or settings.feishu_chat_id
    
    if not app_id or not app_secret:
        return {
            "success": False,
            "error": "Feishu app_id or app_secret not configured. Please set it in settings."
        }
    
    if not chat_id:
        return {
            "success": False,
            "error": "Feishu chat_id not configured. Please set it in settings."
        }
    
    feishu_bot.configure(app_id, app_secret, settings.feishu_encrypt_key or "", settings.feishu_verification_token or "")
    
    result = await feishu_bot.send_message(chat_id, message)
    return result

async def send_feishu_card(card_content: Dict[str, Any], receive_id: Optional[str] = None) -> dict:
    settings = load_settings()
    
    app_id = settings.feishu_app_id
    app_secret = settings.feishu_app_secret
    chat_id = receive_id or settings.feishu_chat_id
    
    if not app_id or not app_secret:
        return {
            "success": False,
            "error": "Feishu app_id or app_secret not configured."
        }
    
    if not chat_id:
        return {
            "success": False,
            "error": "Feishu chat_id not configured."
        }
    
    feishu_bot.configure(app_id, app_secret, settings.feishu_encrypt_key or "", settings.feishu_verification_token or "")
    
    result = await feishu_bot.send_card(chat_id, card_content)
    return result

async def send_feishu_file(file_path: str, receive_id: Optional[str] = None, caption: str = "") -> dict:
    settings = load_settings()
    
    app_id = settings.feishu_app_id
    app_secret = settings.feishu_app_secret
    chat_id = receive_id or settings.feishu_chat_id
    
    if not app_id or not app_secret:
        return {
            "success": False,
            "error": "Feishu app_id or app_secret not configured."
        }
    
    if not chat_id:
        return {
            "success": False,
            "error": "Feishu chat_id not configured."
        }
    
    feishu_bot.configure(app_id, app_secret, settings.feishu_encrypt_key or "", settings.feishu_verification_token or "")
    
    import os
    if not os.path.exists(file_path):
        return {
            "success": False,
            "error": f"File not found: {file_path}"
        }
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    file_type = "file"
    if file_ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]:
        file_type = "image"
    
    file_key = await feishu_bot.upload_file(file_path, file_type)
    
    if not file_key:
        return {
            "success": False,
            "error": "Failed to upload file to Feishu"
        }
    
    if file_type == "image":
        content = json.dumps({"image_key": file_key}, ensure_ascii=False)
        msg_type = "image"
    else:
        content = json.dumps({"file_key": file_key, "file_name": os.path.basename(file_path)}, ensure_ascii=False)
        msg_type = "file"
    
    result = await feishu_bot.send_message(chat_id, content, msg_type)
    return result

async def send_feishu_rich_text(title: str, content: str, receive_id: Optional[str] = None) -> dict:
    settings = load_settings()
    
    app_id = settings.feishu_app_id
    app_secret = settings.feishu_app_secret
    chat_id = receive_id or settings.feishu_chat_id
    
    if not app_id or not app_secret:
        return {
            "success": False,
            "error": "Feishu app_id or app_secret not configured."
        }
    
    if not chat_id:
        return {
            "success": False,
            "error": "Feishu chat_id not configured."
        }
    
    feishu_bot.configure(app_id, app_secret, settings.feishu_encrypt_key or "", settings.feishu_verification_token or "")
    
    rich_content = {
        "zh_cn": {
            "title": title,
            "content": [
                [
                    {
                        "tag": "text",
                        "text": content
                    }
                ]
            ]
        }
    }
    
    content_json = json.dumps(rich_content, ensure_ascii=False)
    
    result = await feishu_bot.send_message(chat_id, content_json, "post")
    return result
