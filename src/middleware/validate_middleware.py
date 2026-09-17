from functools import wraps

from flask import request

from src.utils.response_utils import error


def require_json(*fields):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            data = request.get_json(silent=True)
            if not isinstance(data, dict):
                return error("Request body must be valid JSON")
            missing = [field for field in fields if data.get(field) in (None, "")]
            if missing:
                return error("Missing required fields", details={"fields": missing})
            return view(*args, **kwargs)
        return wrapped
    return decorator
