"""调用 Claude 生成回复，并按用户保存对话上下文（内存中，重启丢失）。"""
import threading
from collections import defaultdict

import anthropic

from . import settings

_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
_history = defaultdict(list)
_lock = threading.Lock()


def reply(user_id: str, text: str) -> str:
    if text.strip() in ("/reset", "清空", "重置"):
        with _lock:
            _history.pop(user_id, None)
        return "已清空对话上下文。"

    with _lock:
        messages = _history[user_id] + [{"role": "user", "content": text}]
    resp = _client.messages.create(
        model=settings.CLAUDE_MODEL,
        max_tokens=1500,
        system=settings.SYSTEM_PROMPT,
        messages=messages,
    )
    answer = "".join(b.text for b in resp.content if b.type == "text") or "（无回复）"

    with _lock:
        h = _history[user_id]
        h.extend([{"role": "user", "content": text}, {"role": "assistant", "content": answer}])
        del h[: -settings.MAX_HISTORY_TURNS * 2]
    return answer
