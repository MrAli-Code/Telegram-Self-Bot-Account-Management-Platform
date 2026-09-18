import os
import sys
from celery import Celery
from celery.schedules import crontab

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings

celery_app = Celery(
    "telegram_bot_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,
    task_soft_time_limit=3000,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    beat_schedule={
        "check-scheduled-tasks": {
            "task": "worker.tasks.check_scheduled_tasks",
            "schedule": crontab(minute="*"),
        },
        "check-repeaters": {
            "task": "worker.tasks.check_repeaters",
            "schedule": crontab(minute="*"),
        },
        "archive-stories": {
            "task": "worker.tasks.archive_stories",
            "schedule": crontab(minute=0, hour="*/6"),
        },
        "monitor-profiles": {
            "task": "worker.tasks.monitor_profiles",
            "schedule": crontab(minute=0, hour="*/1"),
        },
        "cleanup-logs": {
            "task": "worker.tasks.cleanup_old_logs",
            "schedule": crontab(minute=0, hour=3),
        },
    },
)


@celery_app.task(name="worker.tasks.check_scheduled_tasks")
def check_scheduled_tasks():
    return {"status": "checked"}


@celery_app.task(name="worker.tasks.check_repeaters")
def check_repeaters():
    return {"status": "checked"}


@celery_app.task(name="worker.tasks.archive_stories")
def archive_stories():
    return {"status": "archived"}


@celery_app.task(name="worker.tasks.monitor_profiles")
def monitor_profiles():
    return {"status": "monitored"}


@celery_app.task(name="worker.tasks.cleanup_old_logs")
def cleanup_old_logs():
    return {"status": "cleaned"}


@celery_app.task(name="worker.tasks.send_message")
def send_message_task(entity_id: int, message: str):
    return {"status": "sent", "entity": entity_id}


@celery_app.task(name="worker.tasks.download_media")
def download_media_task(message_id: int, file_path: str):
    return {"status": "downloaded", "path": file_path}


@celery_app.task(name="worker.tasks.broadcast")
def broadcast_task(broadcast_id: str):
    return {"status": "broadcast_complete", "id": broadcast_id}


@celery_app.task(name="worker.tasks.create_backup")
def create_backup_task(backup_id: str):
    return {"status": "backup_complete", "id": backup_id}


@celery_app.task(name="worker.tasks.run_conversion")
def run_conversion_task(task_id: str):
    return {"status": "conversion_complete", "id": task_id}
