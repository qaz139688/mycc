import os
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "memory.md")

def ensure_memory_file():
    if not os.path.exists(MEMORY_FILE):
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        default_content = """# AI 记忆存储

> 这是AI的长期记忆系统。AI自主管理这些记忆，无需用户告知。

## 用户信息


## 偏好设置


## 重要事件


## 待办事项


## 其他记忆
"""
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            f.write(default_content)

def read_memory() -> str:
    ensure_memory_file()
    with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def write_memory(content: str) -> None:
    ensure_memory_file()
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

def add_memory(section: str, content: str) -> dict:
    ensure_memory_file()
    memory_content = read_memory()
    
    section_header = f"## {section}"
    
    if section_header not in memory_content:
        memory_content += f"\n\n{section_header}\n\n{content}\n"
    else:
        lines = memory_content.split('\n')
        new_lines = []
        found_section = False
        inserted = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            
            if line.strip() == section_header.strip():
                found_section = True
            elif found_section and not inserted:
                if line.startswith('## ') or i == len(lines) - 1:
                    new_lines.insert(len(new_lines) - 1, f"\n{content}\n")
                    inserted = True
        
        memory_content = '\n'.join(new_lines)
    
    write_memory(memory_content)
    return {"success": True, "message": f"已添加记忆到 {section}"}

def update_memory(section: str, old_content: str, new_content: str) -> dict:
    ensure_memory_file()
    memory_content = read_memory()
    
    if old_content in memory_content:
        memory_content = memory_content.replace(old_content, new_content)
        write_memory(memory_content)
        return {"success": True, "message": f"已更新 {section} 中的记忆"}
    else:
        return {"success": False, "error": "未找到要更新的内容"}

def delete_memory(section: str, content: str) -> dict:
    ensure_memory_file()
    memory_content = read_memory()
    
    if content in memory_content:
        memory_content = memory_content.replace(content, "")
        memory_content = memory_content.replace("\n\n\n", "\n\n")
        write_memory(memory_content)
        return {"success": True, "message": f"已删除 {section} 中的记忆"}
    else:
        return {"success": False, "error": "未找到要删除的内容"}

def get_memory_sections() -> List[str]:
    ensure_memory_file()
    content = read_memory()
    
    sections = []
    for line in content.split('\n'):
        if line.startswith('## '):
            sections.append(line[3:].strip())
    
    return sections

def get_section_content(section: str) -> str:
    ensure_memory_file()
    content = read_memory()
    
    section_header = f"## {section}"
    lines = content.split('\n')
    
    in_section = False
    section_lines = []
    
    for line in lines:
        if line.strip() == section_header.strip():
            in_section = True
            continue
        elif in_section:
            if line.startswith('## '):
                break
            section_lines.append(line)
    
    return '\n'.join(section_lines).strip()

def get_memory_summary() -> str:
    ensure_memory_file()
    content = read_memory()
    
    lines = content.split('\n')
    summary_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('>'):
            summary_lines.append(line)
    
    return '\n'.join(summary_lines)
