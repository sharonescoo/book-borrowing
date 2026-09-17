import os
from datetime import datetime, timedelta, timezone

import jwt


def _secret():
    return os.getenv("JWT_SECRET_KEY", os.getenv("SECRET_KEY", "change-me"))


def create_access_token(admin):
    now = datetime.now(timezone.utc)
    payload = {"sub": str(admin["id"]), "username": admin["username"], "iat": now, "exp": now + timedelta(hours=int(os.getenv("JWT_EXPIRES_HOURS", "24")))}
    return jwt.encode(payload, _secret(), algorithm="HS256")


def decode_access_token(token):
    return jwt.decode(token, _secret(), algorithms=["HS256"])
