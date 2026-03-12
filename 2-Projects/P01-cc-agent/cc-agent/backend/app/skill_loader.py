import os
import json
import logging
import asyncio
import re
from typing import Dict, Optional, List, Any, Set
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from app.skill_models import (
    SkillMetadata, SkillParameter, SkillExample,
    SkillResource, SkillScript, Skill, SkillSummary, SkillActivationResult
)

logger = logging.getLogger(__name__)

SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "skills")

class SkillInstance:
    def __init__(self, skill_dir: str):
        self.skill_dir = skill_dir
        self.id = os.path.basename(skill_dir)
        self.metadata: Optional[SkillMetadata] = None
        self.system_prompt: str = ""
        self.parameters: List[SkillParameter] = []
        self.examples: List[SkillExample] = []
        self.resources: List[SkillResource] = []
        self.scripts: List[SkillScript] = []
        self.last_modified: float = 0
        self._loaded_full: bool = False
        self.load_metadata()
    
    def load_metadata(self):
        skill_file = os.path.join(self.skill_dir, "SKILL.md")
        if not os.path.exists(skill_file):
            skill_file = os.path.join(self.skill_dir, "skill.md")
        
        if not os.path.exists(skill_file):
            logger.warning(f"Skill file not found: {skill_file}")
            return
        
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.last_modified = os.path.getmtime(skill_file)
            self._parse_frontmatter(content)
            logger.info(f"Loaded skill metadata: {self.id} - {self.metadata.name if self.metadata else 'No metadata'}")
        except Exception as e:
            logger.error(f"Failed to load skill {self.skill_dir}: {e}")
    
    def load_full(self):
        if self._loaded_full:
            return
        
        skill_file = os.path.join(self.skill_dir, "SKILL.md")
        if not os.path.exists(skill_file):
            skill_file = os.path.join(self.skill_dir, "skill.md")
        
        if not os.path.exists(skill_file):
            return
        
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self._parse_full_content(content)
            self._load_resources()
            self._loaded_full = True
            logger.info(f"Loaded full skill content: {self.id}")
        except Exception as e:
            logger.error(f"Failed to load full skill {self.skill_dir}: {e}")
    
    def _parse_frontmatter(self, content: str):
        frontmatter = self._extract_frontmatter(content)
        
        if frontmatter:
            self.metadata = SkillMetadata(
                name=frontmatter.get('name', self.id),
                description=frontmatter.get('description', ''),
                version=frontmatter.get('version', '1.0.0'),
                author=frontmatter.get('author', 'system'),
                enabled=frontmatter.get('enabled', 'true').lower() == 'true',
                tags=frontmatter.get('tags', '').split(',') if isinstance(frontmatter.get('tags'), str) else frontmatter.get('tags', []),
                priority=frontmatter.get('priority', 0)
            )
        else:
            self.metadata = SkillMetadata(
                name=self.id.replace('_', ' ').title(),
                description="",
                enabled=True
            )
    
    def _extract_frontmatter(self, content: str) -> Dict[str, Any]:
        lines = content.split('\n')
        if not lines or not lines[0].strip().startswith('---'):
            return {}
        
        frontmatter = {}
        in_frontmatter = False
        
        for i, line in enumerate(lines[1:], 1):
            if line.strip().startswith('---'):
                break
            
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                
                if value.startswith('[') and value.endswith(']'):
                    value = [v.strip().strip('"\'') for v in value[1:-1].split(',') if v.strip()]
                
                frontmatter[key] = value
        
        return frontmatter
    
    def _parse_full_content(self, content: str):
        lines = content.split('\n')
        in_frontmatter = False
        content_lines = []
        current_section = None
        section_content = []
        
        for line in lines:
            if line.strip().startswith('---'):
                in_frontmatter = not in_frontmatter
                continue
            
            if not in_frontmatter:
                if line.startswith('# ') and not line.startswith('## '):
                    if current_section and section_content:
                        self._process_section(current_section, section_content)
                    current_section = line[2:].strip()
                    section_content = []
                elif line.startswith('## '):
                    if current_section and section_content:
                        self._process_section(current_section, section_content)
                    current_section = line[3:].strip()
                    section_content = []
                else:
                    section_content.append(line)
        
        if current_section and section_content:
            self._process_section(current_section, section_content)
        
        self.system_prompt = '\n'.join(content_lines).strip()
    
    def _process_section(self, section_name: str, content: List[str]):
        section_lower = section_name.lower()
        content_str = '\n'.join(content).strip()
        
        if 'parameter' in section_lower or '参数' in section_lower:
            self._parse_parameters(content)
        elif 'example' in section_lower or '示例' in section_lower:
            self._parse_examples(content)
        elif 'resource' in section_lower or '资源' in section_lower:
            self._parse_resources(content)
        elif 'script' in section_lower or '脚本' in section_lower:
            self._parse_scripts(content)
        else:
            if not self.system_prompt:
                self.system_prompt = f"# {section_name}\n\n{content_str}"
            else:
                self.system_prompt += f"\n\n## {section_name}\n\n{content_str}"
    
    def _parse_parameters(self, content: List[str]):
        for line in content:
            line = line.strip()
            if line.startswith('- ') or line.startswith('* '):
                param_str = line[2:].strip()
                parts = param_str.split(':', 1)
                if len(parts) == 2:
                    self.parameters.append(SkillParameter(
                        name=parts[0].strip(),
                        description=parts[1].strip()
                    ))
            elif line.startswith('|') and '|' in line[1:]:
                cells = [c.strip() for c in line.split('|') if c.strip()]
                if len(cells) >= 2 and cells[0].lower() not in ['name', '参数名', '参数']:
                    self.parameters.append(SkillParameter(
                        name=cells[0],
                        description=cells[1] if len(cells) > 1 else '',
                        type=cells[2] if len(cells) > 2 else 'string',
                        required=cells[3].lower() == 'true' if len(cells) > 3 else True
                    ))
    
    def _parse_examples(self, content: List[str]):
        current_input = ""
        current_output = ""
        current_explanation = ""
        
        for line in content:
            line = line.strip()
            if line.lower().startswith('input:') or line.lower().startswith('输入:'):
                if current_input and current_output:
                    self.examples.append(SkillExample(
                        input=current_input,
                        output=current_output,
                        explanation=current_explanation
                    ))
                current_input = line.split(':', 1)[1].strip()
                current_output = ""
                current_explanation = ""
            elif line.lower().startswith('output:') or line.lower().startswith('输出:'):
                current_output = line.split(':', 1)[1].strip()
            elif line.lower().startswith('explanation:') or line.lower().startswith('解释:'):
                current_explanation = line.split(':', 1)[1].strip()
        
        if current_input and current_output:
            self.examples.append(SkillExample(
                input=current_input,
                output=current_output,
                explanation=current_explanation
            ))
    
    def _parse_resources(self, content: List[str]):
        for line in content:
            line = line.strip()
            if line.startswith('- ') or line.startswith('* '):
                resource_str = line[2:].strip()
                parts = resource_str.split(':', 1)
                if len(parts) == 2:
                    self.resources.append(SkillResource(
                        path=parts[0].strip(),
                        type='reference',
                        description=parts[1].strip()
                    ))
    
    def _parse_scripts(self, content: List[str]):
        for line in content:
            line = line.strip()
            if line.startswith('- ') or line.startswith('* '):
                script_str = line[2:].strip()
                parts = script_str.split(':', 1)
                if len(parts) == 2:
                    self.scripts.append(SkillScript(
                        name=parts[0].strip(),
                        path=parts[1].strip()
                    ))
    
    def _load_resources(self):
        for resource in self.resources:
            resource_path = os.path.join(self.skill_dir, resource.path)
            if os.path.exists(resource_path):
                try:
                    with open(resource_path, 'r', encoding='utf-8') as f:
                        resource.content = f.read()
                except Exception as e:
                    logger.error(f"Failed to load resource {resource_path}: {e}")
    
    def get_system_prompt(self) -> str:
        self.load_full()
        return self.system_prompt
    
    def get_summary(self) -> SkillSummary:
        return SkillSummary(
            id=self.id,
            name=self.metadata.name if self.metadata else self.id,
            description=self.metadata.description if self.metadata else "",
            version=self.metadata.version if self.metadata else "1.0.0",
            author=self.metadata.author if self.metadata else "system",
            tags=self.metadata.tags if self.metadata else [],
            enabled=self.metadata.enabled if self.metadata else True
        )


class SkillLoader:
    def __init__(self):
        self.skills: Dict[str, SkillInstance] = {}
        self.observer: Optional[Observer] = None
        self._running = False
    
    def ensure_skills_dir(self):
        if not os.path.exists(SKILLS_DIR):
            os.makedirs(SKILLS_DIR)
    
    def _create_default_skills(self):
        skill_creator_dir = os.path.join(SKILLS_DIR, "skill_creator")
        os.makedirs(skill_creator_dir, exist_ok=True)
        os.makedirs(os.path.join(skill_creator_dir, "references"), exist_ok=True)
        
        skill_content = '''---
name: 技能创建器
description: 帮助用户创建新的AI技能，自动生成标准格式的技能配置
version: 1.0.0
author: system
enabled: true
tags: [skill, create, tool]
---

# 技能创建器

你是一个专业的技能创建助手。你的任务是帮助用户创建符合标准的 AI Agent Skill。

## 何时使用此技能

当用户需要创建新的 AI 技能时，使用此技能指导创建过程。

## 技能标准结构

一个标准的 Skill 包含以下目录结构：

```
skill_name/
├── SKILL.md           # 必需：技能主文件（元数据 + 指令）
├── references/        # 可选：参考文档
│   └── *.md
├── scripts/           # 可选：可执行脚本
│   └── *.py
└── assets/            # 可选：资源文件
    └── templates/
```

## SKILL.md 文件格式

```markdown
---
name: 技能名称
description: 技能描述（用于判断是否激活此技能）
version: 1.0.0
author: 作者名
enabled: true
tags: [tag1, tag2]
---

# 技能名称

## 何时使用此技能

描述什么情况下应该使用这个技能。

## 如何执行任务

详细的执行步骤和指导。

## 参数说明

| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| param1 | string | 是 | 参数说明 |

## 示例

输入: 用户输入示例
输出: 期望输出示例
解释: 为什么这样处理

## 注意事项

- 注意事项1
- 注意事项2
```

## 创建流程

1. 了解用户想要创建什么技能
2. 分析技能需要的能力
3. 设计技能的元数据（name, description）
4. 编写详细的系统提示词和执行指导
5. 使用 file_operation 工具创建技能目录和文件
6. 技能文件保存在: `data/skills/技能名称/SKILL.md`

## 设计原则

### 渐进式披露

- **元数据层**：启动时加载 name 和 description（~100 tokens）
- **指令层**：技能激活时加载完整 SKILL.md（<5000 tokens）
- **资源层**：按需加载 references/assets

### 技能激活

技能由 AI 模型自己判断是否需要激活，不需要触发关键词。AI 会根据 description 判断技能是否与当前任务相关。

请帮助用户创建他们需要的技能！
'''
        skill_path = os.path.join(skill_creator_dir, "SKILL.md")
        with open(skill_path, 'w', encoding='utf-8') as f:
            f.write(skill_content)
        
        faq_content = '''# 技能创建常见问题

## 如何写好技能描述？

技能描述应该：
- 清晰说明技能的作用
- 描述适用场景
- 让 AI 能准确判断何时使用

## 系统提示词应该包含什么？

一个好的系统提示词应该包含：
1. 角色定义：AI 扮演什么角色
2. 能力边界：能做什么，不能做什么
3. 执行流程：具体的操作步骤
4. 质量标准：输出的质量要求
5. 注意事项：需要避免的问题

## 如何使用参考文档？

参考文档用于提供额外的背景知识：
- 放在 references/ 目录下
- 在 SKILL.md 中引用：`[references/doc.md](references/doc.md)`
- 系统会在需要时自动加载
'''
        faq_path = os.path.join(skill_creator_dir, "references", "faq.md")
        with open(faq_path, 'w', encoding='utf-8') as f:
            f.write(faq_content)
        
        logger.info("Created default skill: skill_creator")
    
    def load_all_skills(self):
        self.ensure_skills_dir()
        
        if not os.listdir(SKILLS_DIR):
            self._create_default_skills()
        
        for item in os.listdir(SKILLS_DIR):
            skill_dir = os.path.join(SKILLS_DIR, item)
            if os.path.isdir(skill_dir):
                skill = SkillInstance(skill_dir)
                if skill.metadata:
                    self.skills[skill.id] = skill
        
        logger.info(f"Loaded {len(self.skills)} skills")
    
    def start_watching(self):
        if self._running:
            return
        
        self.ensure_skills_dir()
        self.load_all_skills()
        
        class SkillFileHandler(FileSystemEventHandler):
            def __init__(self, loader):
                self.loader = loader
            
            def on_modified(self, event: FileSystemEvent):
                if event.src_path.endswith('.md'):
                    skill_dir = os.path.dirname(event.src_path)
                    if os.path.dirname(skill_dir) == SKILLS_DIR:
                        logger.info(f"Skill file modified: {skill_dir}")
                        skill = SkillInstance(skill_dir)
                        if skill.metadata:
                            self.loader.skills[skill.id] = skill
            
            def on_created(self, event: FileSystemEvent):
                if event.src_path.endswith('.md'):
                    skill_dir = os.path.dirname(event.src_path)
                    if os.path.dirname(skill_dir) == SKILLS_DIR:
                        logger.info(f"Skill file created: {skill_dir}")
                        skill = SkillInstance(skill_dir)
                        if skill.metadata:
                            self.loader.skills[skill.id] = skill
            
            def on_deleted(self, event: FileSystemEvent):
                if event.src_path.endswith('.md'):
                    skill_dir = os.path.dirname(event.src_path)
                    skill_id = os.path.basename(skill_dir)
                    if skill_id in self.loader.skills:
                        del self.loader.skills[skill_id]
        
        self.observer = Observer()
        self.observer.schedule(SkillFileHandler(self), SKILLS_DIR, recursive=True)
        self.observer.start()
        self._running = True
        logger.info("Skill loader started watching for changes")
    
    def stop_watching(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self._running = False
            logger.info("Skill loader stopped")
    
    def get_skill(self, skill_id: str) -> Optional[SkillInstance]:
        return self.skills.get(skill_id)
    
    def get_all_skills(self) -> List[SkillInstance]:
        return list(self.skills.values())
    
    def get_skills_info(self) -> List[Dict[str, Any]]:
        return [skill.get_summary().model_dump() for skill in self.skills.values()]
    
    def activate_skill(self, skill_id: str) -> SkillActivationResult:
        skill = self.skills.get(skill_id)
        if not skill:
            return SkillActivationResult(
                skill_id=skill_id,
                skill_name="",
                activated=False,
                reason="Skill not found"
            )
        
        if not skill.metadata.enabled:
            return SkillActivationResult(
                skill_id=skill_id,
                skill_name=skill.metadata.name,
                activated=False,
                reason="Skill is disabled"
            )
        
        skill.load_full()
        
        loaded_resources = []
        for resource in skill.resources:
            if hasattr(resource, 'content'):
                loaded_resources.append(resource.path)
        
        return SkillActivationResult(
            skill_id=skill_id,
            skill_name=skill.metadata.name,
            activated=True,
            reason="Skill activated successfully",
            loaded_content=skill.system_prompt,
            loaded_resources=loaded_resources
        )
    
    def create_skill(self, name: str, description: str, system_prompt: str,
                    version: str = "1.0.0", author: str = "user",
                    tags: List[str] = None) -> SkillInstance:
        self.ensure_skills_dir()
        
        skill_id = name.lower().replace(' ', '_').replace('-', '_')
        skill_id = ''.join(c for c in skill_id if c.isalnum() or c == '_')
        
        skill_dir = os.path.join(SKILLS_DIR, skill_id)
        os.makedirs(skill_dir, exist_ok=True)
        os.makedirs(os.path.join(skill_dir, "references"), exist_ok=True)
        
        tags_str = str(tags) if tags else "[]"
        
        content = f'''---
name: {name}
description: {description}
version: {version}
author: {author}
enabled: true
tags: {tags_str}
---

# {name}

{system_prompt}
'''
        
        skill_file = os.path.join(skill_dir, "SKILL.md")
        with open(skill_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        skill = SkillInstance(skill_dir)
        self.skills[skill.id] = skill
        logger.info(f"Created skill: {skill.id}")
        return skill
    
    def delete_skill(self, skill_id: str) -> bool:
        if skill_id in self.skills:
            skill = self.skills[skill_id]
            if os.path.exists(skill.skill_dir):
                import shutil
                shutil.rmtree(skill.skill_dir)
            del self.skills[skill_id]
            logger.info(f"Deleted skill: {skill_id}")
            return True
        return False
    
    def get_skills_metadata_prompt(self) -> str:
        if not self.skills:
            return ""
        
        lines = ["# 可用技能列表\n"]
        lines.append("以下是当前可用的技能，根据 description 判断是否需要激活：\n")
        for skill in self.skills.values():
            if skill.metadata and skill.metadata.enabled:
                lines.append(f"- **{skill.metadata.name}**: {skill.metadata.description}")
        
        return '\n'.join(lines)

skill_loader = SkillLoader()
