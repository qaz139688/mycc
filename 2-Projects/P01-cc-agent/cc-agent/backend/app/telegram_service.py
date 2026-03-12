import httpx
import logging
import os
from typing import Optional

from app.config import load_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_proxy_url() -> Optional[str]:
    http_proxy = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    https_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    return https_proxy or http_proxy

def create_async_client(**kwargs) -> httpx.AsyncClient:
    if "trust_env" not in kwargs:
        kwargs["trust_env"] = True
    proxy_url = get_proxy_url()
    if proxy_url:
        kwargs["proxy"] = proxy_url
    return httpx.AsyncClient(**kwargs)

async def send_telegram_message(message: str) -> dict:
    settings = load_settings()
    
    token = settings.telegram_token
    chat_id = settings.telegram_chat_id
    
    if not token:
        return {
            "success": False,
            "error": "Telegram token not configured. Please set it in settings."
        }
    
    if not chat_id:
        return {
            "success": False,
            "error": "Telegram chat_id not configured. Please set it in settings."
        }
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    try:
        async with create_async_client() as client:
            response = await client.post(
                url,
                json={
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "HTML"
                },
                timeout=30
            )
            
            result = response.json()
            
            if result.get("ok"):
                logger.info(f"Telegram message sent successfully to chat_id: {chat_id}")
                return {
                    "success": True,
                    "message_id": result.get("result", {}).get("message_id")
                }
            else:
                error_desc = result.get("description", "Unknown error")
                logger.error(f"Telegram API error: {error_desc}")
                return {
                    "success": False,
                    "error": error_desc
                }
    
    except httpx.TimeoutException:
        logger.error("Telegram API timeout")
        return {
            "success": False,
            "error": "Request timeout"
        }
    except Exception as e:
        logger.error(f"Telegram send error: {e}")
        return {
            "success": False,
            "error": str(e)
        }

async def send_telegram_photo(photo_url: str, caption: Optional[str] = None) -> dict:
    settings = load_settings()
    
    token = settings.telegram_token
    chat_id = settings.telegram_chat_id
    
    if not token or not chat_id:
        return {
            "success": False,
            "error": "Telegram not configured"
        }
    
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    
    try:
        async with create_async_client() as client:
            data = {
                "chat_id": chat_id,
                "photo": photo_url
            }
            if caption:
                data["caption"] = caption
                data["parse_mode"] = "HTML"
            
            response = await client.post(url, json=data, timeout=30)
            result = response.json()
            
            if result.get("ok"):
                logger.info(f"Telegram photo sent successfully")
                return {
                    "success": True,
                    "message_id": result.get("result", {}).get("message_id")
                }
            else:
                return {
                    "success": False,
                    "error": result.get("description", "Unknown error")
                }
    
    except Exception as e:
        logger.error(f"Telegram send photo error: {e}")
        return {
            "success": False,
            "error": str(e)
        }
