import httpx
import logging
import asyncio
import os
from typing import Optional, Callable, Awaitable
from datetime import datetime

from app.config import load_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

FILES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "1052")

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
        logger.debug(f"Using proxy: {proxy_url}")
    return httpx.AsyncClient(**kwargs)

def ensure_files_dir():
    if not os.path.exists(FILES_DIR):
        os.makedirs(FILES_DIR)

class TelegramBot:
    def __init__(self):
        self.token: Optional[str] = None
        self.chat_id: Optional[str] = None
        self.running: bool = False
        self.last_update_id: int = 0
        self.message_handler: Optional[Callable[[str, str], Awaitable[str]]] = None
        self._task: Optional[asyncio.Task] = None
    
    def configure(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id
        logger.info(f"Telegram bot configured for chat_id: {chat_id}")
    
    def set_message_handler(self, handler: Callable[[str, str], Awaitable[str]]):
        self.message_handler = handler
    
    async def start(self):
        if not self.token:
            logger.error("Cannot start bot: token not configured")
            return False
        
        ensure_files_dir()
        self.running = True
        self._task = asyncio.create_task(self._poll_loop())
        logger.info("Telegram bot started")
        return True
    
    def stop(self):
        self.running = False
        if self._task:
            self._task.cancel()
            self._task = None
        logger.info("Telegram bot stopped")
    
    async def _poll_loop(self):
        logger.info("Telegram bot poll loop started")
        while self.running:
            try:
                await self._get_updates()
            except Exception as e:
                logger.error(f"Poll error: {e}")
            await asyncio.sleep(1)
        logger.info("Telegram bot poll loop stopped")
    
    async def _get_updates(self):
        url = f"https://api.telegram.org/bot{self.token}/getUpdates"
        params = {
            "offset": self.last_update_id + 1,
            "timeout": 30
        }
        
        try:
            async with create_async_client() as client:
                response = await client.get(url, params=params, timeout=35)
                result = response.json()
                
                if not result.get("ok"):
                    logger.error(f"getUpdates error: {result.get('description')}")
                    return
                
                updates = result.get("result", [])
                
                for update in updates:
                    self.last_update_id = update.get("update_id", 0)
                    
                    if "message" in update:
                        message = update["message"]
                        chat_id = str(message.get("chat", {}).get("id", ""))
                        user_name = message.get("from", {}).get("first_name", "User")
                        
                        if chat_id == self.chat_id:
                            text = message.get("text", "")
                            
                            if text:
                                logger.info(f"Received message from {user_name}: {text}")
                                
                                if self.message_handler:
                                    try:
                                        await self.message_handler(text, user_name)
                                    except Exception as e:
                                        logger.error(f"Message handler error: {e}")
                                        await self.send_message(f"处理消息时出错: {str(e)}")
                            
                            elif "document" in message:
                                await self._handle_document(message, user_name)
                            
                            elif "photo" in message:
                                await self._handle_photo(message, user_name)
                            
                            elif "audio" in message:
                                await self._handle_audio(message, user_name)
                            
                            elif "video" in message:
                                await self._handle_video(message, user_name)
        
        except httpx.TimeoutException:
            pass
        except Exception as e:
            logger.error(f"getUpdates exception: {e}")
    
    async def _handle_document(self, message: dict, user_name: str):
        document = message.get("document", {})
        file_id = document.get("file_id")
        file_name = document.get("file_name", f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        file_size = document.get("file_size", 0)
        
        logger.info(f"Received document from {user_name}: {file_name} ({file_size} bytes)")
        
        try:
            file_path = await self._download_file(file_id, file_name)
            if file_path:
                await self.send_message(f"文件已保存: {file_name}\n路径: 1052/{file_name}")
                
                if self.message_handler:
                    await self.message_handler(f"[文件接收] 用户 {user_name} 发送了文件: {file_name}", user_name)
        except Exception as e:
            logger.error(f"Failed to download document: {e}")
            await self.send_message(f"文件下载失败: {str(e)}")
    
    async def _handle_photo(self, message: dict, user_name: str):
        photos = message.get("photo", [])
        if not photos:
            return
        
        largest_photo = photos[-1]
        file_id = largest_photo.get("file_id")
        file_name = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        
        logger.info(f"Received photo from {user_name}")
        
        try:
            file_path = await self._download_file(file_id, file_name)
            if file_path:
                await self.send_message(f"图片已保存: {file_name}\n路径: 1052/{file_name}")
        except Exception as e:
            logger.error(f"Failed to download photo: {e}")
            await self.send_message(f"图片下载失败: {str(e)}")
    
    async def _handle_audio(self, message: dict, user_name: str):
        audio = message.get("audio", {})
        file_id = audio.get("file_id")
        file_name = audio.get("file_name", f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3")
        
        logger.info(f"Received audio from {user_name}: {file_name}")
        
        try:
            file_path = await self._download_file(file_id, file_name)
            if file_path:
                await self.send_message(f"音频已保存: {file_name}\n路径: 1052/{file_name}")
        except Exception as e:
            logger.error(f"Failed to download audio: {e}")
            await self.send_message(f"音频下载失败: {str(e)}")
    
    async def _handle_video(self, message: dict, user_name: str):
        video = message.get("video", {})
        file_id = video.get("file_id")
        file_name = video.get("file_name", f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
        
        logger.info(f"Received video from {user_name}: {file_name}")
        
        try:
            file_path = await self._download_file(file_id, file_name)
            if file_path:
                await self.send_message(f"视频已保存: {file_name}\n路径: 1052/{file_name}")
        except Exception as e:
            logger.error(f"Failed to download video: {e}")
            await self.send_message(f"视频下载失败: {str(e)}")
    
    async def _download_file(self, file_id: str, file_name: str) -> Optional[str]:
        ensure_files_dir()
        
        get_file_url = f"https://api.telegram.org/bot{self.token}/getFile"
        
        async with create_async_client() as client:
            response = await client.get(get_file_url, params={"file_id": file_id}, timeout=30)
            result = response.json()
            
            if not result.get("ok"):
                logger.error(f"getFile error: {result.get('description')}")
                return None
            
            file_path_remote = result.get("result", {}).get("file_path")
            if not file_path_remote:
                logger.error("No file_path in response")
                return None
            
            download_url = f"https://api.telegram.org/file/bot{self.token}/{file_path_remote}"
            
            file_path_local = os.path.join(FILES_DIR, file_name)
            
            download_response = await client.get(download_url, timeout=300)
            
            if download_response.status_code == 200:
                with open(file_path_local, "wb") as f:
                    f.write(download_response.content)
                logger.info(f"File saved: {file_path_local}")
                return file_path_local
            else:
                logger.error(f"Download failed: {download_response.status_code}")
                return None
    
    async def send_message(self, message: str) -> dict:
        if not self.token or not self.chat_id:
            return {"success": False, "error": "Bot not configured"}
        
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        
        try:
            async with create_async_client() as client:
                response = await client.post(
                    url,
                    json={
                        "chat_id": self.chat_id,
                        "text": message,
                        "parse_mode": "HTML"
                    },
                    timeout=30
                )
                
                result = response.json()
                
                if result.get("ok"):
                    logger.info(f"Message sent successfully")
                    return {"success": True, "message_id": result.get("result", {}).get("message_id")}
                else:
                    error_desc = result.get("description", "Unknown error")
                    logger.error(f"sendMessage error: {error_desc}")
                    return {"success": False, "error": error_desc}
        
        except Exception as e:
            import traceback
            logger.error(f"sendMessage exception: {e}\n{traceback.format_exc()}")
            return {"success": False, "error": str(e)}
    
    async def send_document(self, file_path: str, caption: str = "") -> dict:
        if not self.token or not self.chat_id:
            return {"success": False, "error": "Bot not configured"}
        
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}
        
        url = f"https://api.telegram.org/bot{self.token}/sendDocument"
        
        try:
            with open(file_path, "rb") as f:
                file_content = f.read()
            
            file_name = os.path.basename(file_path)
            
            boundary = f"----WebKitFormBoundary{os.urandom(8).hex()}"
            
            body_parts = []
            body_parts.append(f'--{boundary}\r\n')
            body_parts.append(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n')
            body_parts.append(f'{self.chat_id}\r\n')
            
            if caption:
                body_parts.append(f'--{boundary}\r\n')
                body_parts.append(f'Content-Disposition: form-data; name="caption"\r\n\r\n')
                body_parts.append(f'{caption}\r\n')
            
            body_parts.append(f'--{boundary}\r\n')
            body_parts.append(f'Content-Disposition: form-data; name="document"; filename="{file_name}"\r\n')
            body_parts.append(f'Content-Type: application/octet-stream\r\n\r\n')
            
            body = ''.join(body_parts).encode('utf-8') + file_content + f'\r\n--{boundary}--\r\n'.encode('utf-8')
            
            headers = {
                'Content-Type': f'multipart/form-data; boundary={boundary}'
            }
            
            async with create_async_client(timeout=300) as client:
                response = await client.post(url, content=body, headers=headers)
                
                result = response.json()
                
                if result.get("ok"):
                    logger.info(f"Document sent successfully: {file_path}")
                    return {"success": True, "message_id": result.get("result", {}).get("message_id")}
                else:
                    error_desc = result.get("description", "Unknown error")
                    logger.error(f"sendDocument error: {error_desc}")
                    return {"success": False, "error": error_desc}
        
        except Exception as e:
            logger.error(f"sendDocument exception: {e}")
            return {"success": False, "error": str(e)}
    
    async def send_photo(self, file_path: str, caption: str = "") -> dict:
        if not self.token or not self.chat_id:
            return {"success": False, "error": "Bot not configured"}
        
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File not found: {file_path}"}
        
        url = f"https://api.telegram.org/bot{self.token}/sendPhoto"
        
        try:
            with open(file_path, "rb") as f:
                file_content = f.read()
            
            file_name = os.path.basename(file_path)
            
            async with create_async_client(timeout=300) as client:
                files = {"photo": (file_name, file_content)}
                data = {"chat_id": self.chat_id}
                if caption:
                    data["caption"] = caption
                
                response = await client.post(url, data=data, files=files)
                
                result = response.json()
                
                if result.get("ok"):
                    logger.info(f"Photo sent successfully: {file_path}")
                    return {"success": True, "message_id": result.get("result", {}).get("message_id")}
                else:
                    error_desc = result.get("description", "Unknown error")
                    logger.error(f"sendPhoto error: {error_desc}")
                    return {"success": False, "error": error_desc}
        
        except Exception as e:
            logger.error(f"sendPhoto exception: {e}")
            return {"success": False, "error": str(e)}

telegram_bot = TelegramBot()
