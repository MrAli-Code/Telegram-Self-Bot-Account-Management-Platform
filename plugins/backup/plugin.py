from backend.app.services.backup import BackupService, backup_service

manifest = {
    "name": "Backup Plugin",
    "version": "1.0.0",
    "description": "Full backup and restore engine",
    "author": "Telegram Self-Bot",
    "permissions": ["read_messages", "read_media"],
    "enabled": True,
}

config = {
    "supported_formats": ["zip", "json", "html", "txt", "csv"],
    "encryption": True,
    "compression": True,
}


class BackupPlugin:
    def __init__(self):
        self.service = backup_service

    async def create(self, **kwargs):
        return await self.service.create_backup(**kwargs)

    async def restore(self, backup_id):
        return await self.service.restore_backup(backup_id)


__all__ = ["BackupPlugin", "manifest", "config"]
