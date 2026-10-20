# 企业微信 + Claude 机器人

个人微信通过「企业微信互通」直接和这个机器人聊天（官方支持，不封号）。

```
个人微信 ⇄ 企业微信应用 ⇄ 本服务 (/wecom/callback) ⇄ Claude API
```

## 1. 企业微信后台配置
1. 注册企业微信（免费）：https://work.weixin.qq.com
2. 「应用管理」→ 创建自建应用，记下 **AgentId**、**Secret**；「我的企业」页记下 **CorpID**。
3. 应用页 →「接收消息」→ 设置 API 接收：随机生成 **Token** 和 **EncodingAESKey**，**先不要保存**，等服务跑起来再点保存（保存时会触发 URL 验证）。
4. 应用页 →「企业可信 IP」填写服务器公网 IP（否则发送消息会报 60020）。
5. 让个人微信和机器人聊天：「客户联系」→「客户」→「微信插件」，用个人微信扫码关注企业；
   或在「通讯录」邀请自己的微信。

## 2. 运行
```bash
pip install -r wecom_bot/requirements.txt
export WECOM_CORP_ID=... WECOM_AGENT_ID=... WECOM_SECRET=...
export WECOM_TOKEN=... WECOM_ENCODING_AES_KEY=...
export ANTHROPIC_API_KEY=...
uvicorn wecom_bot.server:app --host 0.0.0.0 --port 8000
```
需要公网 HTTPS 地址。本地调试可用 `ngrok http 8000`，
回调 URL 填 `https://<域名>/wecom/callback`，回到后台点保存。

## 可选环境变量
- `CLAUDE_MODEL`（默认 claude-sonnet-5-5）、`BOT_SYSTEM_PROMPT`
- `ALLOWED_USERS`：逗号分隔的 userid 白名单，建议设置，防止他人消耗你的额度
- `MAX_HISTORY_TURNS`（默认 10）、`MAX_INPUT_CHARS`（默认 4000）

聊天中发送 `/reset` 可清空上下文。

## 注意
- 上下文保存在内存，重启即丢失；多进程部署需换成 Redis 等。
- 聊天内容会发送给 Claude API，请确认符合你的数据合规要求。
