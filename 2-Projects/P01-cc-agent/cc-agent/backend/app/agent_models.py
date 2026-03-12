from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime

class AgentMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: Optional[int] = None

class AgentChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    context: Optional[List[AgentMessage]] = None
    metadata: Optional[Dict[str, Any]] = None

class AgentChatResponse(BaseModel):
    success: bool
    conversation_id: str
    response: str
    agent_id: str
    agent_name: str
    timestamp: int
    tool_calls: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None

class AgentInfo(BaseModel):
    agent_id: str
    agent_name: str
    version: str
    capabilities: List[str]
    description: str
    endpoints: List[Dict[str, str]]

class AgentToolCall(BaseModel):
    tool_id: str
    tool_name: str
    arguments: Dict[str, Any]
    result: Optional[str] = None

class AgentStreamChunk(BaseModel):
    type: Literal["content", "tool_call", "tool_result", "done", "error"]
    content: Optional[str] = None
    tool_call: Optional[AgentToolCall] = None
    error: Optional[str] = None

class AgentCapability(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]
    required: List[str]

class AgentHeartbeat(BaseModel):
    agent_id: str
    status: Literal["online", "busy", "offline"]
    timestamp: int
    current_tasks: int
    uptime_seconds: int

class ACPSettingsUpdate(BaseModel):
    acp_enabled: Optional[bool] = None
    acp_data_path: Optional[str] = None
    acp_seed_password: Optional[str] = None
    acp_access_point: Optional[str] = None
    acp_agent_name: Optional[str] = None
    acp_aid: Optional[str] = None
    acp_debug: Optional[bool] = None

class ACPMessageRequest(BaseModel):
    to_aid: str
    content: str

class ACPMessageResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    error: Optional[str] = None

class ACPStatusResponse(BaseModel):
    enabled: bool
    running: bool
    current_aid: Optional[str] = None
    aid_list: List[str] = []
