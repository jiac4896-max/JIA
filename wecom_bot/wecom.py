"""企业微信 API：获取 access_token、发送应用消息。"""
import threading
import time

import requests

from . import settings

API = "https://qyapi.weixin.qq.com/cgi-bin"
MAX_BYTES = 2000  # 单条文本消息上限 2048 字节，留余量

_lock = threading.Lock()
_token = {"value": "", "expires": 0.0}


def get_access_token() -> str:
    with _lock:
        if _token["value"] and time.time() < _token["expires"]:
            return _token["value"]
        r = requests.get(
            f"{API}/gettoken",
            params={"corpid": settings.WECOM_CORP_ID, "corpsecret": settings.WECOM_SECRET},
            timeout=10,
        ).json()
        if r.get("errcode") != 0:
            raise RuntimeError(f"获取 access_token 失败: {r}")
        _token["value"] = r["access_token"]
        _token["expires"] = time.time() + r["expires_in"] - 120
        return _token["value"]


def _split(text: str):
    chunk, size = [], 0
    for ch in text:
        n = len(ch.encode())
        if size + n > MAX_BYTES:
            yield "".join(chunk)
            chunk, size = [], 0
        chunk.append(ch)
        size += n
    if chunk:
        yield "".join(chunk)


def send_text(user_id: str, text: str) -> None:
    for part in _split(text):
        r = requests.post(
            f"{API}/message/send",
            params={"access_token": get_access_token()},
            json={
                "touser": user_id,
                "msgtype": "text",
                "agentid": int(settings.WECOM_AGENT_ID),
                "text": {"content": part},
            },
            timeout=10,
        ).json()
        if r.get("errcode") != 0:
            raise RuntimeError(f"发送消息失败: {r}")
