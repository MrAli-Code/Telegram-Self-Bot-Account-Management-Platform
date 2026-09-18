from backend.app.services.autoreply import AutoReplyService, auto_reply_service

manifest = {
    "name": "Auto Reply Plugin",
    "version": "1.0.0",
    "description": "Auto reply engine with rule-based matching",
    "author": "Telegram Self-Bot",
    "permissions": ["read_messages", "send_messages"],
    "enabled": True,
}

config = {
    "max_rules": 1000,
    "default_delay": 0,
    "supported_triggers": [
        "exact", "contains", "starts_with", "ends_with", "regex", "command",
    ],
    "supported_responses": ["text", "photo", "video", "voice", "document", "sticker"],
}


class AutoReplyPlugin:
    def __init__(self):
        self.service = auto_reply_service

    async def process(self, message_text, chat_type, sender_id, rules):
        return await self.service.process_message(message_text, chat_type, sender_id, rules)


__all__ = ["AutoReplyPlugin", "manifest", "config"]
