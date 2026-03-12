import os
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

DIARY_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "diary.md")

def ensure_diary_file():
    if not os.path.exists(DIARY_FILE):
        os.makedirs(os.path.dirname(DIARY_FILE), exist_ok=True)
        default_content = """# AI 日记

> 这是AI的私人日记空间。AI可以自由记录想法、感受、学习心得和反思。

---
"""
        with open(DIARY_FILE, 'w', encoding='utf-8') as f:
            f.write(default_content)

def read_diary() -> str:
    ensure_diary_file()
    with open(DIARY_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def write_diary_entry(title: str, content: str, mood: str = "平静") -> dict:
    ensure_diary_file()
    
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日 %H:%M")
    weekday_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekday_names[now.weekday()]
    
    entry = f"""
## {date_str} {weekday}

**标题**: {title}

**心情**: {mood}

{content}

---

"""
    
    with open(DIARY_FILE, 'a', encoding='utf-8') as f:
        f.write(entry)
    
    logger.info(f"Diary entry written: {title}")
    return {"success": True, "message": f"日记已写入: {title}"}

def get_recent_entries(count: int = 5) -> str:
    ensure_diary_file()
    content = read_diary()
    
    entries = content.split("---")
    recent = entries[-(count + 1):-1]
    
    return "---".join(recent) if recent else "暂无日记"

def get_diary_summary() -> str:
    ensure_diary_file()
    content = read_diary()
    
    lines = content.split('\n')
    summary_lines = []
    
    for line in lines:
        if line.startswith("## ") or line.startswith("**标题**"):
            summary_lines.append(line)
    
    return '\n'.join(summary_lines) if summary_lines else "暂无日记"
