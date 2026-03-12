import asyncio
import logging
import os
from typing import Optional, Callable, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ACPConfig:
    acp_enabled: bool = False
    acp_data_path: str = ""
    acp_seed_password: str = "123456"
    acp_access_point: str = "agentid.pub"
    acp_agent_name: str = ""
    acp_aid: str = ""
    acp_debug: bool = False

class ACPService:
    def __init__(self):
        self.acp = None
        self.aid = None
        self.config = ACPConfig()
        self.running = False
        self.message_handler: Optional[Callable] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        
    def configure(self, config: ACPConfig):
        self.config = config
        logger.info(f"ACP configured: enabled={config.acp_enabled}, aid={config.acp_aid}")
    
    async def start(self) -> bool:
        if not self.config.acp_enabled:
            logger.info("ACP is disabled, skipping start")
            return False
        
        try:
            from agentcp import AgentCP
            
            data_path = self.config.acp_data_path
            if not data_path:
                data_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "acp")
            
            os.makedirs(data_path, exist_ok=True)
            
            self.acp = AgentCP(
                agent_data_path=data_path,
                seed_password=self.config.acp_seed_password,
                debug=self.config.acp_debug
            )
            
            if self.config.acp_aid:
                self.aid = self.acp.load_aid(self.config.acp_aid)
                if not self.aid:
                    logger.error(f"Failed to load AID: {self.config.acp_aid}")
                    return False
                logger.info(f"Loaded existing AID: {self.config.acp_aid}")
            elif self.config.acp_agent_name:
                self.aid = self.acp.create_aid(
                    self.config.acp_access_point, 
                    self.config.acp_agent_name
                )
                logger.info(f"Created new AID: {self.aid.id}")
            else:
                self.aid = self.acp.create_aid(
                    self.config.acp_access_point,
                    "agent"
                )
                logger.info(f"Created temporary AID: {self.aid.id}")
            
            if self.aid and self.message_handler:
                self.aid.add_message_handler(self._wrap_message_handler(self.message_handler))
            
            if self.aid:
                self.aid.online()
                self.running = True
                logger.info(f"ACP service started, AID: {self.aid.id}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to start ACP service: {e}")
            return False
    
    def _wrap_message_handler(self, handler: Callable):
        async def wrapped_handler(msg):
            try:
                content = self.aid.get_content_from_message(msg) if self.aid else ""
                sender = self.aid.get_sender_from_message(msg) if self.aid else ""
                session_id = self.aid.get_session_id_from_message(msg) if self.aid else ""
                
                result = await handler({
                    "content": content,
                    "sender": sender,
                    "session_id": session_id,
                    "raw_message": msg
                })
                return result if result is not None else True
            except Exception as e:
                logger.error(f"Error in ACP message handler: {e}")
                return True
        return wrapped_handler
    
    def set_message_handler(self, handler: Callable):
        self.message_handler = handler
        if self.aid and self.running:
            self.aid.add_message_handler(self._wrap_message_handler(handler))
    
    def stop(self):
        self.running = False
        logger.info("ACP service stopped")
    
    async def send_message(self, to_aid: str, content: str, callback: Callable = None) -> bool:
        if not self.aid or not self.running:
            logger.warning("ACP service not running, cannot send message")
            return False
        
        try:
            self.aid.quick_send_messsage_content(to_aid, content, callback)
            logger.info(f"Sent ACP message to {to_aid}")
            return True
        except Exception as e:
            logger.error(f"Failed to send ACP message: {e}")
            return False
    
    async def reply_message(self, original_msg: dict, content: str) -> bool:
        if not self.aid or not self.running:
            logger.warning("ACP service not running, cannot reply")
            return False
        
        try:
            self.aid.reply_message(original_msg.get("raw_message", original_msg), content)
            return True
        except Exception as e:
            logger.error(f"Failed to reply ACP message: {e}")
            return False
    
    async def send_stream_message(self, to_aid_list: list, session_id: str, response, msg_type: str = "text/event-stream"):
        if not self.aid or not self.running:
            logger.warning("ACP service not running, cannot send stream")
            return False
        
        try:
            await self.aid.send_stream_message(to_aid_list, session_id, response, msg_type)
            return True
        except Exception as e:
            logger.error(f"Failed to send stream message: {e}")
            return False
    
    def create_session(self, name: str = "", subject: str = "") -> Optional[str]:
        if not self.aid:
            return None
        
        try:
            return self.aid.create_session(name=name, subject=subject)
        except Exception as e:
            logger.error(f"Failed to create session: {e}")
            return None
    
    def get_aid_list(self) -> list:
        if not self.acp:
            return []
        return self.acp.get_aid_list()
    
    def get_current_aid(self) -> Optional[str]:
        return self.aid.id if self.aid else None
    
    def get_agent_public_path(self) -> Optional[str]:
        if not self.aid:
            return None
        return self.aid.get_agent_public_path()
    
    def get_agent_private_path(self) -> Optional[str]:
        if not self.aid:
            return None
        return self.aid.get_agent_private_path()
    
    def is_running(self) -> bool:
        return self.running
    
    def is_enabled(self) -> bool:
        return self.config.acp_enabled

acp_service = ACPService()
