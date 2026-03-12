import os
import logging
from datetime import datetime
from typing import Optional, List

logger = logging.getLogger(__name__)

NOVEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "小说创作")

def ensure_novel_dir():
    if not os.path.exists(NOVEL_DIR):
        os.makedirs(NOVEL_DIR)

def get_novel_path(novel_name: str) -> str:
    return os.path.join(NOVEL_DIR, novel_name)

def get_chapter_path(novel_name: str, chapter_num: int) -> str:
    novel_path = get_novel_path(novel_name)
    return os.path.join(novel_path, f"第{chapter_num:02d}章.txt")

def create_novel_outline(novel_name: str, outline: str, target_words: int = 3500) -> dict:
    ensure_novel_dir()
    novel_path = get_novel_path(novel_name)
    
    if not os.path.exists(novel_path):
        os.makedirs(novel_path)
    
    outline_file = os.path.join(novel_path, "大纲.txt")
    with open(outline_file, 'w', encoding='utf-8') as f:
        f.write(f"# {novel_name}\n\n")
        f.write(f"目标字数：每章 {target_words} 字\n\n")
        f.write(f"创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("---\n\n")
        f.write(outline)
    
    logger.info(f"Created novel outline: {novel_name}")
    return {"success": True, "message": f"小说《{novel_name}》大纲已创建"}

def save_chapter(novel_name: str, chapter_num: int, title: str, content: str) -> dict:
    ensure_novel_dir()
    novel_path = get_novel_path(novel_name)
    
    if not os.path.exists(novel_path):
        os.makedirs(novel_path)
    
    chapter_file = get_chapter_path(novel_name, chapter_num)
    
    word_count = len(content.replace('\n', '').replace(' ', ''))
    
    full_content = f"第{chapter_num}章 {title}\n\n{content}\n\n---\n字数：{word_count}"
    
    with open(chapter_file, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    progress_file = os.path.join(novel_path, "进度.txt")
    with open(progress_file, 'w', encoding='utf-8') as f:
        f.write(f"当前章节：第{chapter_num}章\n")
        f.write(f"最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"总字数：{word_count}\n")
    
    logger.info(f"Saved chapter {chapter_num} for novel: {novel_name}")
    return {
        "success": True,
        "message": f"第{chapter_num}章已保存",
        "word_count": word_count,
        "file_path": chapter_file
    }

def get_current_chapter(novel_name: str) -> int:
    novel_path = get_novel_path(novel_name)
    if not os.path.exists(novel_path):
        return 0
    
    files = os.listdir(novel_path)
    chapter_files = [f for f in files if f.startswith("第") and f.endswith("章.txt")]
    
    if not chapter_files:
        return 0
    
    chapter_nums = []
    for f in chapter_files:
        try:
            num = int(f[1:3])
            chapter_nums.append(num)
        except:
            pass
    
    return max(chapter_nums) if chapter_nums else 0

def get_novel_status(novel_name: str) -> dict:
    novel_path = get_novel_path(novel_name)
    
    if not os.path.exists(novel_path):
        return {"exists": False, "chapters": 0, "total_words": 0}
    
    files = os.listdir(novel_path)
    chapter_files = [f for f in files if f.startswith("第") and f.endswith("章.txt")]
    
    total_words = 0
    for cf in chapter_files:
        cf_path = os.path.join(novel_path, cf)
        with open(cf_path, 'r', encoding='utf-8') as f:
            content = f.read()
            total_words += len(content.replace('\n', '').replace(' ', ''))
    
    return {
        "exists": True,
        "chapters": len(chapter_files),
        "total_words": total_words,
        "novel_path": novel_path
    }

def get_chapter_content(novel_name: str, chapter_num: int) -> Optional[str]:
    chapter_file = get_chapter_path(novel_name, chapter_num)
    
    if os.path.exists(chapter_file):
        with open(chapter_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None
