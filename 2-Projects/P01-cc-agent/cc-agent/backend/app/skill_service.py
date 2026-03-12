import json
import os
import logging
from typing import List, Optional, Dict, Any
from app.skill_models import Skill, SkillCreate, SkillUpdate

logger = logging.getLogger(__name__)

SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "skills")

def ensure_skills_dir():
    if not os.path.exists(SKILLS_DIR):
        os.makedirs(SKILLS_DIR)

def get_skill_file_path(skill_id: str) -> str:
    return os.path.join(SKILLS_DIR, f"{skill_id}.json")

def load_skill(skill_id: str) -> Optional[Skill]:
    ensure_skills_dir()
    file_path = get_skill_file_path(skill_id)
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return Skill(**data)
        except Exception as e:
            logger.error(f"Failed to load skill {skill_id}: {e}")
    return None

def load_all_skills() -> List[Skill]:
    ensure_skills_dir()
    skills = []
    for filename in os.listdir(SKILLS_DIR):
        if filename.endswith(".json"):
            skill_id = filename[:-5]
            skill = load_skill(skill_id)
            if skill:
                skills.append(skill)
    return skills

def save_skill(skill: Skill) -> None:
    ensure_skills_dir()
    file_path = get_skill_file_path(skill.id)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(skill.model_dump(), f, indent=2, ensure_ascii=False)

def create_skill(create: SkillCreate) -> Skill:
    import time
    current_time = int(time.time() * 1000)
    
    skill_id = create.name.lower().replace(" ", "_").replace("-", "_")
    skill_id = "".join(c for c in skill_id if c.isalnum() or c == "_")
    
    skill = Skill(
        id=skill_id,
        name=create.name,
        description=create.description,
        triggers=create.triggers,
        parameters=create.parameters,
        system_prompt=create.system_prompt,
        user_prompt_template=create.user_prompt_template,
        examples=create.examples,
        created_at=current_time,
        updated_at=current_time
    )
    save_skill(skill)
    return skill

def update_skill(skill_id: str, update: SkillUpdate) -> Optional[Skill]:
    skill = load_skill(skill_id)
    if not skill:
        return None
    
    if update.name is not None:
        skill.name = update.name
    if update.description is not None:
        skill.description = update.description
    if update.triggers is not None:
        skill.triggers = update.triggers
    if update.parameters is not None:
        skill.parameters = update.parameters
    if update.system_prompt is not None:
        skill.system_prompt = update.system_prompt
    if update.user_prompt_template is not None:
        skill.user_prompt_template = update.user_prompt_template
    if update.examples is not None:
        skill.examples = update.examples
    if update.enabled is not None:
        skill.enabled = update.enabled
    
    import time
    skill.updated_at = int(time.time() * 1000)
    save_skill(skill)
    return skill

def delete_skill(skill_id: str) -> bool:
    file_path = get_skill_file_path(skill_id)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

def match_skill(user_input: str, skills: List[Skill]) -> Optional[Skill]:
    user_input_lower = user_input.lower()
    for skill in skills:
        if not skill.enabled:
            continue
        for trigger in skill.triggers:
            if trigger.lower() in user_input_lower:
                return skill
    return None

def format_skill_prompt(skill: Skill, user_input: str, **kwargs) -> Dict[str, str]:
    system_prompt = skill.system_prompt
    
    if skill.examples:
        examples_text = "\n\n## 示例\n\n"
        for i, example in enumerate(skill.examples, 1):
            examples_text += f"### 示例 {i}\n"
            examples_text += f"**输入**: {example.input}\n"
            examples_text += f"**输出**: {example.output}\n"
            if example.explanation:
                examples_text += f"**说明**: {example.explanation}\n"
            examples_text += "\n"
        system_prompt += examples_text
    
    user_prompt = user_input
    if skill.user_prompt_template:
        user_prompt = skill.user_prompt_template.format(
            input=user_input,
            **kwargs
        )
    
    return {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt
    }

def get_skill_creator_prompt() -> str:
    return """# 技能创建器

你是一个专业的技能创建助手。你的任务是帮助用户创建新的AI技能。

## 技能结构说明

一个完整的技能包含以下部分：

1. **name**: 技能名称，简洁明了
2. **description**: 技能描述，说明这个技能的作用
3. **triggers**: 触发词列表，当用户输入包含这些词时会自动触发该技能
4. **parameters**: 参数列表，定义技能需要的参数
   - name: 参数名
   - description: 参数描述
   - type: 参数类型 (string, number, boolean, array, object)
   - required: 是否必需
   - default: 默认值
5. **system_prompt**: 系统提示词，定义AI在该技能下的行为
6. **user_prompt_template**: 用户提示词模板，可使用 {input} 和参数名作为占位符
7. **examples**: 示例列表，帮助AI理解如何使用该技能

## 创建流程

1. 了解用户想要创建什么技能
2. 分析技能需要的参数和触发条件
3. 编写系统提示词和用户提示词模板
4. 提供示例
5. 使用 create_skill 工具创建技能

## 注意事项

- 系统提示词要清晰、具体，包含所有必要的指令
- 触发词要具有代表性，避免过于宽泛
- 参数定义要完整，包含类型和描述
- 示例要覆盖典型使用场景

请帮助用户创建他们需要的技能！"""

def init_default_skills():
    ensure_skills_dir()
    
    skill_creator = load_skill("skill_creator")
    if not skill_creator:
        import time
        current_time = int(time.time() * 1000)
        
        skill_creator = Skill(
            id="skill_creator",
            name="技能创建器",
            description="帮助用户创建新的AI技能，自动生成技能配置和提示词",
            triggers=["创建技能", "新建技能", "添加技能", "创建一个技能", "帮我创建技能"],
            parameters=[
                {
                    "name": "skill_name",
                    "description": "技能名称",
                    "type": "string",
                    "required": True
                },
                {
                    "name": "skill_description",
                    "description": "技能描述",
                    "type": "string",
                    "required": True
                }
            ],
            system_prompt=get_skill_creator_prompt(),
            user_prompt_template="请帮我创建一个技能：{input}",
            examples=[
                {
                    "input": "创建一个翻译技能",
                    "output": "好的，我来帮你创建一个翻译技能。这个技能可以自动检测语言并进行翻译。",
                    "explanation": "用户想要创建翻译功能，需要定义源语言和目标语言参数"
                }
            ],
            enabled=True,
            created_at=current_time,
            updated_at=current_time
        )
        save_skill(skill_creator)
        logger.info("Created default skill: skill_creator")
