import asyncio
import logging
import random
import os
import json
from datetime import datetime
from typing import Optional, Callable, Awaitable

logger = logging.getLogger(__name__)

STATE_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "money_making_state.json")

class MoneyMakingMode:
    def __init__(self):
        self.enabled: bool = False
        self._task: Optional[asyncio.Task] = None
        self._on_write_chapter: Optional[Callable[[str, int, str], Awaitable[None]]] = None
        self._stop_flag: bool = False
        self.current_novel: str = ""
        self.novel_outline: str = ""
        self.target_words: int = 3500
    
    def set_write_chapter_callback(self, callback: Callable[[str, int, str], Awaitable[None]]):
        self._on_write_chapter = callback
    
    def is_enabled(self) -> bool:
        return self.enabled
    
    def save_state(self):
        state = {
            "enabled": self.enabled,
            "current_novel": self.current_novel,
            "novel_outline": self.novel_outline,
            "target_words": self.target_words
        }
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def load_state(self) -> bool:
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                self.current_novel = state.get("current_novel", "")
                self.novel_outline = state.get("novel_outline", "")
                self.target_words = state.get("target_words", 3500)
                return state.get("enabled", False)
            except:
                pass
        return False
    
    def start(self, novel_name: str, outline: str = ""):
        if self.enabled:
            return
        
        self.enabled = True
        self._stop_flag = False
        self.current_novel = novel_name
        self.novel_outline = outline
        self.save_state()
        self._task = asyncio.create_task(self._writing_loop())
        logger.info(f"Money-making mode started for: {novel_name}")
    
    def stop(self):
        self.enabled = False
        self._stop_flag = True
        self.save_state()
        if self._task:
            self._task.cancel()
            self._task = None
        logger.info("Money-making mode stopped")
    
    async def resume(self):
        if self.enabled:
            return
        
        should_resume = self.load_state()
        if should_resume and self.current_novel:
            self.enabled = True
            self._stop_flag = False
            self._task = asyncio.create_task(self._writing_loop())
            logger.info(f"Money-making mode resumed for: {self.current_novel}")
    
    async def _writing_loop(self):
        while self.enabled and not self._stop_flag:
            try:
                from app.novel_service import get_current_chapter, ensure_novel_dir, get_novel_path
                import os
                
                ensure_novel_dir()
                novel_path = get_novel_path(self.current_novel)
                
                if not os.path.exists(novel_path):
                    os.makedirs(novel_path)
                    
                    if self.novel_outline:
                        outline_file = os.path.join(novel_path, "大纲.txt")
                        with open(outline_file, 'w', encoding='utf-8') as f:
                            f.write(f"# {self.current_novel}\n\n")
                            f.write(f"创建时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                            f.write("---\n\n")
                            f.write(self.novel_outline)
                
                current_chapter = get_current_chapter(self.current_novel)
                next_chapter = current_chapter + 1
                
                logger.info(f"Writing chapter {next_chapter} for {self.current_novel}")
                
                if self._on_write_chapter:
                    await self._on_write_chapter(self.current_novel, next_chapter, self.novel_outline)
                
                wait_time = random.randint(300, 600)
                
                for i in range(wait_time):
                    if self._stop_flag or not self.enabled:
                        return
                    await asyncio.sleep(1)
                
                if self._stop_flag or not self.enabled:
                    return
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Writing loop error: {e}")
                await asyncio.sleep(60)

money_making_mode = MoneyMakingMode()
