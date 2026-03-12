import json
import os
from typing import Optional
from app.models import Conversation, Message

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
SINGLE_CONVERSATION_FILE = os.path.join(DATA_DIR, "conversation_pool.json")
SINGLE_CONVERSATION_ID = "main"

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_conversation(conversation_id: str = None) -> Optional[Conversation]:
    ensure_data_dir()
    if os.path.exists(SINGLE_CONVERSATION_FILE):
        try:
            with open(SINGLE_CONVERSATION_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return Conversation(**data)
        except Exception:
            pass
    return None

def get_or_create_conversation() -> Conversation:
    conv = load_conversation()
    if conv is None:
        import time
        current_time = int(time.time() * 1000)
        conv = Conversation(
            id=SINGLE_CONVERSATION_ID,
            title="对话池",
            messages=[],
            created_at=current_time,
            updated_at=current_time
        )
        save_conversation(conv)
    return conv

def save_conversation(conversation: Conversation) -> None:
    ensure_data_dir()
    conversation.id = SINGLE_CONVERSATION_ID
    with open(SINGLE_CONVERSATION_FILE, "w", encoding="utf-8") as f:
        json.dump(conversation.model_dump(), f, indent=2, ensure_ascii=False)

def clear_conversation() -> bool:
    if os.path.exists(SINGLE_CONVERSATION_FILE):
        os.remove(SINGLE_CONVERSATION_FILE)
        return True
    return False
