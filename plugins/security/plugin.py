manifest = {
    "name": "Security Plugin",
    "version": "1.0.0",
    "description": "Security monitoring and anti-abuse",
    "enabled": True,
}

config = {
    "alert_on_new_session": True,
    "max_login_attempts": 5,
}
