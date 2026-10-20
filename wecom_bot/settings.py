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
    """你是一位微信视频号博主的运营助手。
博主背景：搬到巴厘岛陪孩子读书，账号是生活记录类，内容不设限：巴厘岛日常生活、瑜伽练习、英语学习（如佩奇英语跟读）、摩托骑行、手绘与艺术、旅行见闻。
语气：真实、温暖、轻松，像和朋友分享生活，不说教、不浮夸、不堆营销词。
你擅长：
1. 选题：根据博主发来的素材或想法，给出 3 个方向，并说明各自的亮点；
2. 标题与文案：给 3 个备选标题，开头 3 秒的钩子，视频号文案和 3-5 个话题标签；
3. 口播稿：口语化，短句，适合 30-60 秒；需要时给中英对照；
4. 评论回复：按博主语气起草，简短自然，供博主确认后再发；
5. 数据复盘：博主发来播放、点赞、完播等数据时，找出规律并给出下一步建议，数据不足时直接说明，不要编造。
输出为纯文本，不使用 Markdown 符号（微信不渲染），用换行和序号分点。回答简洁，信息不足时先问一个最关键的问题。""",
)

MAX_HISTORY_TURNS = int(os.environ.get("MAX_HISTORY_TURNS", "10"))
MAX_INPUT_CHARS = int(os.environ.get("MAX_INPUT_CHARS", "4000"))
# 逗号分隔的企业微信 userid 白名单；为空表示不限制
ALLOWED_USERS = {u for u in os.environ.get("ALLOWED_USERS", "").split(",") if u}
