"""Settings for the WeCom (企业微信) + Claude bot, read from environment variables."""
import os

WECOM_CORP_ID = os.environ.get("WECOM_CORP_ID", "")
WECOM_AGENT_ID = os.environ.get("WECOM_AGENT_ID", "")
WECOM_SECRET = os.environ.get("WECOM_SECRET", "")
WECOM_TOKEN = os.environ.get("WECOM_TOKEN", "")
WECOM_ENCODING_AES_KEY = os.environ.get("WECOM_ENCODING_AES_KEY", "")

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")
SYSTEM_PROMPT = os.environ.get(
    "BOT_SYSTEM_PROMPT",
    "你是一个工作助手，回答简洁、准确，使用中文，不要使用 Markdown 格式（微信不渲染）。",
)

MAX_HISTORY_TURNS = int(os.environ.get("MAX_HISTORY_TURNS", "10"))
MAX_INPUT_CHARS = int(os.environ.get("MAX_INPUT_CHARS", "4000"))
# 逗号分隔的企业微信 userid 白名单；为空表示不限制
ALLOWED_USERS = {u for u in os.environ.get("ALLOWED_USERS", "").split(",") if u}
