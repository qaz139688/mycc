from pydantic import BaseModel, ConfigDict
from typing import Literal, Optional, List
from datetime import datetime

class Message(BaseModel):
    role: str
    content: str
    timestamp: int

class Conversation(BaseModel):
    id: str
    title: str
    messages: List[Message]
    created_at: int
    updated_at: int

class SendMessageRequest(BaseModel):
    conversation_id: Optional[str] = None
    content: str

class SendMessageResponse(BaseModel):
    conversation_id: str
    user_message: Message
    assistant_message: Message

class SettingsUpdate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    api_key: Optional[str] = None
    api_base_url: Optional[str] = None
    model_name: Optional[str] = None
    telegram_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    metaso_api_key: Optional[str] = None
    user_custom_prompt: Optional[str] = None
    user_preferences: Optional[str] = None
    personality_file: Optional[str] = None
    personality_content: Optional[str] = None
    feishu_app_id: Optional[str] = None
    feishu_app_secret: Optional[str] = None
    feishu_encrypt_key: Optional[str] = None
    feishu_verification_token: Optional[str] = None
    feishu_chat_id: Optional[str] = None
    acp_enabled: Optional[bool] = None
    acp_data_path: Optional[str] = None
    acp_seed_password: Optional[str] = None
    acp_access_point: Optional[str] = None
    acp_agent_name: Optional[str] = None
    acp_aid: Optional[str] = None
    acp_debug: Optional[bool] = None

class SettingsResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    api_key: str
    api_base_url: str
    model_name: str
    telegram_token: str
    telegram_chat_id: str
    metaso_api_key: str
    user_custom_prompt: str
    user_preferences: str
    personality_file: str
    personality_content: str
    feishu_app_id: str
    feishu_app_secret: str
    feishu_encrypt_key: str
    feishu_verification_token: str
    feishu_chat_id: str
    acp_enabled: bool = False
    acp_data_path: str = ""
    acp_seed_password: str = ""
    acp_access_point: str = "agentid.pub"
    acp_agent_name: str = ""
    acp_aid: str = ""
    acp_debug: bool = False

class NativeCommandRequest(BaseModel):
    command: str
    shell_type: Literal['cmd', 'powershell']
    timeout: Optional[int] = 30

class NativeCommandResponse(BaseModel):
    success: bool
    output: str
    error: Optional[str] = None
    exit_code: Optional[int] = None

class NativeCommandLog(BaseModel):
    id: str
    command: str
    shell_type: str
    output: str
    error: Optional[str]
    exit_code: Optional[int]
    timestamp: datetime
    duration: float

class FileOperationRequest(BaseModel):
    operation: Literal['read', 'write', 'append', 'delete', 'list', 'exists', 'edit', 'replace']
    path: str
    content: Optional[str] = None
    encoding: Optional[str] = 'utf-8'
    line_number: Optional[int] = None
    old_text: Optional[str] = None
    new_text: Optional[str] = None

class FileOperationResponse(BaseModel):
    success: bool
    content: Optional[str] = None
    files: Optional[List[str]] = None
    exists: Optional[bool] = None
    error: Optional[str] = None
