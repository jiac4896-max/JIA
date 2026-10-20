"""企业微信回调服务：验签 -> 立即返回 -> 后台调用 Claude -> 主动推送回复。"""
import logging
import xml.etree.ElementTree as ET
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse

from . import ai, settings, wecom
from .crypto import WeComCrypto, WeComCryptoError

log = logging.getLogger("wecom_bot")
app = FastAPI()
crypto = WeComCrypto(settings.WECOM_TOKEN, settings.WECOM_ENCODING_AES_KEY, settings.WECOM_CORP_ID)
pool = ThreadPoolExecutor(max_workers=8)
_seen = OrderedDict()  # 企业微信 5 秒内无响应会重试，用 MsgId 去重


def _is_duplicate(msg_id: str) -> bool:
    if msg_id in _seen:
        return True
    _seen[msg_id] = None
    if len(_seen) > 2000:
        _seen.popitem(last=False)
    return False


def _handle(user_id: str, text: str) -> None:
    try:
        wecom.send_text(user_id, ai.reply(user_id, text))
    except Exception:
        log.exception("处理消息失败")
        try:
            wecom.send_text(user_id, "抱歉，处理出错了，请稍后再试。")
        except Exception:
            log.exception("错误提示发送失败")


@app.get("/wecom/callback", response_class=PlainTextResponse)
def verify_url(
    msg_signature: str = Query(...),
    timestamp: str = Query(...),
    nonce: str = Query(...),
    echostr: str = Query(...),
):
    """配置"接收消息"时企业微信会发来的 URL 验证请求。"""
    try:
        crypto.verify(msg_signature, timestamp, nonce, echostr)
        return crypto.decrypt(echostr)
    except WeComCryptoError as e:
        raise HTTPException(403, str(e))


@app.post("/wecom/callback", response_class=PlainTextResponse)
async def receive(
    request: Request,
    msg_signature: str = Query(...),
    timestamp: str = Query(...),
    nonce: str = Query(...),
):
    body = (await request.body()).decode()
    try:
        encrypted = ET.fromstring(body).findtext("Encrypt", "")
        crypto.verify(msg_signature, timestamp, nonce, encrypted)
        msg = ET.fromstring(crypto.decrypt(encrypted))
    except (WeComCryptoError, ET.ParseError, ValueError) as e:
        raise HTTPException(403, str(e))

    user_id = msg.findtext("FromUserName", "")
    msg_id = msg.findtext("MsgId", "")
    if msg.findtext("MsgType") != "text" or _is_duplicate(msg_id):
        return "success"
    if settings.ALLOWED_USERS and user_id not in settings.ALLOWED_USERS:
        return "success"

    text = msg.findtext("Content", "")[: settings.MAX_INPUT_CHARS]
    pool.submit(_handle, user_id, text)
    return "success"
