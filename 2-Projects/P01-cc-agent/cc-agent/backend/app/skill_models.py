from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SkillParameter(BaseModel):
    name: str
    description: str
    type: str = "string"
    required: bool = True
    default: Optional[str] = None
    enum: Optional[List[str]] = None

class SkillExample(BaseModel):
    input: str
    output: str
    explanation: Optional[str] = None

class SkillMetadata(BaseModel):
    name: str
    description: str
    version: str = "1.0.0"
    author: str = "system"
    enabled: bool = True
    tags: List[str] = []
    priority: int = 0

class SkillResource(BaseModel):
    path: str
    type: str
    description: str = ""

class SkillScript(BaseModel):
    name: str
    path: str
    description: str = ""
    parameters: List[SkillParameter] = []

class Skill(BaseModel):
    id: str
    metadata: SkillMetadata
    system_prompt: str
    parameters: List[SkillParameter] = []
    examples: List[SkillExample] = []
    resources: List[SkillResource] = []
    scripts: List[SkillScript] = []
    created_at: int
    updated_at: int

class SkillCreate(BaseModel):
    name: str
    description: str
    system_prompt: str
    version: str = "1.0.0"
    author: str = "user"
    tags: List[str] = []
    parameters: List[SkillParameter] = []
    examples: List[SkillExample] = []
    resources: List[SkillResource] = []
    scripts: List[SkillScript] = []

class SkillUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    system_prompt: Optional[str] = None
    tags: Optional[List[str]] = None
    parameters: Optional[List[SkillParameter]] = None
    examples: Optional[List[SkillExample]] = None
    resources: Optional[List[SkillResource]] = None
    scripts: Optional[List[SkillScript]] = None
    enabled: Optional[bool] = None

class SkillSummary(BaseModel):
    id: str
    name: str
    description: str
    version: str
    author: str
    tags: List[str]
    enabled: bool

class SkillActivationResult(BaseModel):
    skill_id: str
    skill_name: str
    activated: bool
    reason: str = ""
    loaded_content: str = ""
    loaded_resources: List[str] = []
