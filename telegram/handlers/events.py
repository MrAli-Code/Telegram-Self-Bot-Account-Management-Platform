from telethon import events, typed
import logging
import re
from datetime import datetime

logger = logging.getLogger("telegram_bot.handlers")


class UpdateHandler:
    def __init__(self, client, db_session=None):
        self.client = client
        self.db = db_session
        self._handlers_registered = False

    def register(self):
        if self._handlers_registered:
            return
        self.client.on(events.NewMessage)(self.handle_new_message)
        self.client.on(events.MessageDeleted)(self.handle_deleted_message)
        self.client.on(events.MessageEdited)(self.handle_edited_message)
        self.client.on(events.UserUpdate)(self.handle_user_update)
        self._handlers_registered = True
        logger.info("Event handlers registered")

    async def handle_new_message(self, event: events.NewMessage.Event):
        try:
            message = event.message
            chat = await event.get_chat()
            sender = await event.get_sender()

            logger.debug(
                f"New message in {getattr(chat, 'title', 'DM')}: "
                f"{message.text[:50] if message.text else '[media]'}"
            )
        except Exception as e:
            logger.error(f"Error handling new message: {e}")

    async def handle_deleted_message(self, event: events.MessageDeleted.Event):
        try:
            logger.info(f"Message deleted: IDs {event.deleted_ids} in chat {event.chat_id}")
        except Exception as e:
            logger.error(f"Error handling deleted message: {e}")

    async def handle_edited_message(self, event: events.MessageEdited.Event):
        try:
            message = event.message
            logger.debug(f"Message edited: {message.id}")
        except Exception as e:
            logger.error(f"Error handling edited message: {e}")

    async def handle_user_update(self, event: events.UserUpdate.Event):
        try:
            user = event.user
            logger.debug(f"User update: {user.id}")
        except Exception as e:
            logger.error(f"Error handling user update: {e}")
