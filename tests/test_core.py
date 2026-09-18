import pytest
from backend.app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, decode_token,
)


def test_password_hashing():
    password = "test_password_123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong_password", hashed)


def test_access_token():
    data = {"sub": "user123", "username": "testuser"}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "user123"
    assert payload["type"] == "access"


def test_refresh_token():
    data = {"sub": "user123"}
    token = create_refresh_token(data)
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "user123"
    assert payload["type"] == "refresh"


def test_decode_invalid_token():
    result = decode_token("invalid.token.here")
    assert result is None


def test_auto_reply_matching():
    from backend.app.services.autoreply import AutoReplyService
    service = AutoReplyService()

    class MockRule:
        trigger_type = "exact"
        trigger_value = "hello"
        is_enabled = True
        chat_scope = "all"
        user_scope = "all"
        allowed_users = []
        blocked_users = []
        working_hours_start = None
        working_hours_end = None
        max_replies = None
        reply_count = 0

    rule = MockRule()
    assert service.match_rule("hello", rule) is True
    assert service.match_rule("Hello", rule) is True
    assert service.match_rule("hello world", rule) is False

    rule.trigger_type = "contains"
    rule.trigger_value = "hello"
    assert service.match_rule("say hello world", rule) is True
    assert service.match_rule("goodbye", rule) is False

    rule.trigger_type = "regex"
    rule.trigger_value = r"\bhello\b"
    assert service.match_rule("hello there", rule) is True


def test_anti_abuse():
    from backend.app.services.security.antispam import AntiAbuseService
    service = AntiAbuseService()

    assert service.is_stopped() is False
    assert service.check_rate_limit("test", 100) is True

    service.emergency_stop()
    assert service.is_stopped() is True
    assert service.check_rate_limit("test", 100) is False

    service.reset_emergency_stop()
    assert service.is_stopped() is False


def test_scheduler():
    from backend.app.services.scheduler import SchedulerService
    scheduler = SchedulerService()
    assert scheduler is not None


def test_websocket_manager():
    from backend.app.services.websocket import ConnectionManager
    manager = ConnectionManager()
    assert len(manager.active_connections) == 0
    assert len(manager._subscriptions) == 0
