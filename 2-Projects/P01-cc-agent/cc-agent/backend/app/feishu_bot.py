import httpx
import logging
import asyncio
import hashlib
import hmac
import base64
import json
from typing import Optional, Callable, Awaitable, Dict, Any
from datetime import datetime

from app.config import load_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeishuBot:
    def __init__(self):
        self.app_id: Optional[str] = None
        self.app_secret: Optional[str] = None
        self.encrypt_key: Optional[str] = None
        self.verification_token: Optional[str] = None
        self.tenant_access_token: Optional[str] = None
        self.token_expires_at: int = 0
        self.running: bool = False
        self.message_handler: Optional[Callable[[str, str], Awaitable[str]]] = None
        self._task: Optional[asyncio.Task] = None
    
    def configure(self, app_id: str, app_secret: str, encrypt_key: str = "", verification_token: str = ""):
        self.app_id = app_id
        self.app_secret = app_secret
        self.encrypt_key = encrypt_key
        self.verification_token = verification_token
        logger.info(f"Feishu bot configured for app_id: {app_id}")
    
    def set_message_handler(self, handler: Callable[[str, str], Awaitable[str]]):
        self.message_handler = handler
    
    async def start(self):
        if not self.app_id or not self.app_secret:
            logger.error("Cannot start bot: app_id or app_secret not configured")
            return False
        
        self.running = True
        self._task = asyncio.create_task(self._token_refresh_loop())
        logger.info("Feishu bot started")
        return True
    
    def stop(self):
        self.running = False
        if self._task:
            self._task.cancel()
            self._task = None
        logger.info("Feishu bot stopped")
    
    async def _token_refresh_loop(self):
        while self.running:
            try:
                await self._ensure_token()
                await asyncio.sleep(300)
            except Exception as e:
                logger.error(f"Token refresh error: {e}")
                await asyncio.sleep(60)
    
    async def _ensure_token(self):
        current_time = int(datetime.now().timestamp())
        if self.tenant_access_token and current_time < self.token_expires_at - 300:
            return
        
        await self._refresh_tenant_token()
    
    async def _refresh_tenant_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url,
                    json={
                        "app_id": self.app_id,
                        "app_secret": self.app_secret
                    },
                    timeout=30
                )
                
                result = response.json()
                
                if result.get("code") == 0:
                    self.tenant_access_token = result.get("tenant_access_token")
                    expire_in = result.get("expire", 7200)
                    self.token_expires_at = int(datetime.now().timestamp()) + expire_in
                    logger.info("Tenant access token refreshed successfully")
                else:
                    logger.error(f"Failed to refresh token: {result.get('msg')}")
        
        except Exception as e:
            logger.error(f"Token refresh exception: {e}")
    
    def verify_url(self, challenge: str) -> Optional[str]:
        if not self.verification_token:
            return None
        
        if challenge != self.verification_token:
            logger.warning("Verification token mismatch")
            return None
        
        return challenge
    
    def decrypt_event(self, encrypt: str) -> Optional[Dict[str, Any]]:
        if not self.encrypt_key:
            return json.loads(encrypt)
        
        try:
            key = base64.b64decode(self.encrypt_key + "=")
            cipher_text = base64.b64decode(encrypt)
            
            iv = cipher_text[:16]
            encrypted_data = cipher_text[16:-16]
            tag = cipher_text[-16:]
            
            from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
            from cryptography.hazmat.backends import default_backend
            
            cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            
            decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
            
            event_data = json.loads(decrypted.decode('utf-8'))
            return event_data
        
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            return None
    
    async def handle_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            event_type = event_data.get("header", {}).get("event_type")
            
            if event_type == "im.message.receive_v1":
                await self._handle_message_event(event_data)
            
            return {"code": 0, "msg": "success"}
        
        except Exception as e:
            logger.error(f"Event handling error: {e}")
            return {"code": 1, "msg": str(e)}
    
    async def _handle_message_event(self, event_data: Dict[str, Any]):
        try:
            event = event_data.get("event", {})
            message = event.get("message", {})
            sender = event.get("sender", {})
            
            chat_id = message.get("chat_id")
            message_id = message.get("message_id")
            content = message.get("content", "{}")
            msg_type = message.get("msg_type")
            
            sender_id = sender.get("sender_id", {}).get("open_id", "")
            sender_name = sender.get("sender_type", "unknown")
            
            if msg_type == "text":
                content_json = json.loads(content)
                text = content_json.get("text", "")
                
                logger.info(f"Received message from {sender_name} ({sender_id}): {text}")
                
                if self.message_handler:
                    try:
                        await self.message_handler(text, sender_name)
                    except Exception as e:
                        logger.error(f"Message handler error: {e}")
                        await self.send_message(chat_id, f"处理消息时出错: {str(e)}")
            
            elif msg_type == "file":
                content_json = json.loads(content)
                file_key = content_json.get("file_key", "")
                file_name = content_json.get("file_name", "unknown")
                
                logger.info(f"Received file from {sender_name}: {file_name}")
                
                if self.message_handler:
                    await self.message_handler(f"[文件接收] 用户 {sender_name} 发送了文件: {file_name}", sender_name)
            
            elif msg_type == "image":
                content_json = json.loads(content)
                image_key = content_json.get("image_key", "")
                
                logger.info(f"Received image from {sender_name}")
                
                if self.message_handler:
                    await self.message_handler(f"[图片接收] 用户 {sender_name} 发送了一张图片", sender_name)
        
        except Exception as e:
            logger.error(f"Message event handling error: {e}")
    
    async def send_message(self, receive_id: str, content: str, msg_type: str = "text", receive_id_type: str = "chat_id") -> Dict[str, Any]:
        await self._ensure_token()
        
        if not self.tenant_access_token:
            return {"success": False, "error": "Token not available"}
        
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        
        try:
            content_json = json.dumps({"text": content}, ensure_ascii=False)
            
            params = {"receive_id_type": receive_id_type}
            
            headers = {
                "Authorization": f"Bearer {self.tenant_access_token}",
                "Content-Type": "application/json; charset=utf-8"
            }
            
            payload = {
                "receive_id": receive_id,
                "msg_type": msg_type,
                "content": content_json
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, params=params, headers=headers, json=payload, timeout=30)
                
                result = response.json()
                
                if result.get("code") == 0:
                    logger.info(f"Message sent successfully to {receive_id}")
                    return {"success": True, "message_id": result.get("data", {}).get("message_id")}
                else:
                    error_msg = result.get("msg", "Unknown error")
                    logger.error(f"Send message error: {error_msg}")
                    return {"success": False, "error": error_msg}
        
        except Exception as e:
            logger.error(f"Send message exception: {e}")
            return {"success": False, "error": str(e)}
    
    async def send_card(self, receive_id: str, card_content: Dict[str, Any], receive_id_type: str = "chat_id") -> Dict[str, Any]:
        await self._ensure_token()
        
        if not self.tenant_access_token:
            return {"success": False, "error": "Token not available"}
        
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        
        try:
            content_json = json.dumps(card_content, ensure_ascii=False)
            
            params = {"receive_id_type": receive_id_type}
            
            headers = {
                "Authorization": f"Bearer {self.tenant_access_token}",
                "Content-Type": "application/json; charset=utf-8"
            }
            
            payload = {
                "receive_id": receive_id,
                "msg_type": "interactive",
                "content": content_json
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, params=params, headers=headers, json=payload, timeout=30)
                
                result = response.json()
                
                if result.get("code") == 0:
                    logger.info(f"Card sent successfully to {receive_id}")
                    return {"success": True, "message_id": result.get("data", {}).get("message_id")}
                else:
                    error_msg = result.get("msg", "Unknown error")
                    logger.error(f"Send card error: {error_msg}")
                    return {"success": False, "error": error_msg}
        
        except Exception as e:
            logger.error(f"Send card exception: {e}")
            return {"success": False, "error": str(e)}
    
    async def upload_file(self, file_path: str, file_type: str = "file") -> Optional[str]:
        await self._ensure_token()
        
        if not self.tenant_access_token:
            return None
        
        url = f"https://open.feishu.cn/open-apis/im/v1/{file_type}s"
        
        try:
            import os
            
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return None
            
            with open(file_path, "rb") as f:
                file_content = f.read()
            
            file_name = os.path.basename(file_path)
            
            headers = {
                "Authorization": f"Bearer {self.tenant_access_token}"
            }
            
            files = {
                "file": (file_name, file_content)
            }
            
            async with httpx.AsyncClient(timeout=300) as client:
                response = await client.post(url, headers=headers, files=files)
                
                result = response.json()
                
                if result.get("code") == 0:
                    file_key = result.get("data", {}).get("file_key")
                    logger.info(f"File uploaded successfully: {file_name} -> {file_key}")
                    return file_key
                else:
                    error_msg = result.get("msg", "Unknown error")
                    logger.error(f"Upload file error: {error_msg}")
                    return None
        
        except Exception as e:
            logger.error(f"Upload file exception: {e}")
            return None

feishu_bot = FeishuBot()