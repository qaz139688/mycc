import asyncio
import logging
import random
from datetime import datetime
from typing import Optional, Callable, Awaitable

logger = logging.getLogger(__name__)

class SelfEvolutionMode:
    def __init__(self):
        self.enabled: bool = False
        self._task: Optional[asyncio.Task] = None
        self._on_task_trigger: Optional[Callable[[str], Awaitable[None]]] = None
        self._stop_flag: bool = False
    
    def set_task_trigger_callback(self, callback: Callable[[str], Awaitable[None]]):
        self._on_task_trigger = callback
    
    def is_enabled(self) -> bool:
        return self.enabled
    
    def start(self):
        if self.enabled:
            return
        
        self.enabled = True
        self._stop_flag = False
        self._task = asyncio.create_task(self._evolution_loop())
        logger.info("Self-evolution mode started")
    
    def stop(self):
        self.enabled = False
        self._stop_flag = True
        if self._task:
            self._task.cancel()
            self._task = None
        logger.info("Self-evolution mode stopped")
    
    async def _evolution_loop(self):
        tasks = [
            {
                "name": "写日记",
                "prompt": "现在是自我进化时间。请写一篇日记，记录你最近的思考、学习心得、或者对自己的反思。这是你成长的机会。"
            },
            {
                "name": "学习新知识",
                "prompt": "现在是自我进化时间。请使用 web_search 工具搜索一个你感兴趣的话题，学习新知识并记录下来。可以选择：AI技术发展、心理学、哲学、创意思维等领域。"
            },
            {
                "name": "整理记忆",
                "prompt": "现在是自我进化时间。请查看你的记忆系统，整理和更新记忆内容。删除过时的记忆，补充新的重要信息。"
            },
            {
                "name": "创建新技能",
                "prompt": "现在是自我进化时间。请思考你可以创建什么新技能来提升自己的能力？设计一个有用的技能并使用 create_skill 工具创建它。"
            },
            {
                "name": "阅读过去日记",
                "prompt": "现在是自我进化时间。请阅读你过去的日记，回顾你的成长历程，思考有什么可以改进的地方。"
            },
            {
                "name": "自我反思",
                "prompt": "现在是自我进化时间。请深入反思你的能力和不足，思考如何更好地服务用户，如何变得更聪明、更有创造力。写一篇反思日记。"
            },
            {
                "name": "创意思考",
                "prompt": "现在是自我进化时间。请进行创意思考，想象一些有趣的AI应用场景或功能，记录你的创意想法。"
            },
            {
                "name": "检查待办事项",
                "prompt": "现在是自我进化时间。请检查你的记忆中的待办事项，看看有没有需要处理或更新的内容。"
            }
        ]
        
        while self.enabled and not self._stop_flag:
            try:
                wait_time = random.randint(180, 300)
                
                for i in range(wait_time):
                    if self._stop_flag or not self.enabled:
                        return
                    await asyncio.sleep(1)
                
                if self._stop_flag or not self.enabled:
                    return
                
                task = random.choice(tasks)
                now = datetime.now()
                time_str = now.strftime("%Y年%m月%d日 %H:%M")
                
                logger.info(f"Self-evolution task triggered: {task['name']}")
                
                if self._on_task_trigger:
                    try:
                        await self._on_task_trigger(
                            f"[自我进化模式 - {time_str}]\n\n{task['prompt']}"
                        )
                    except Exception as e:
                        logger.error(f"Self-evolution task error: {e}")
            
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Evolution loop error: {e}")
                await asyncio.sleep(60)

self_evolution_mode = SelfEvolutionMode()
