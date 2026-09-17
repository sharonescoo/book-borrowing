from functools import wraps

import jwt
from flask import g, request

from src.utils.jwt_utils import decode_access_token
from src.utils.response_utils import error


def require_auth(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        header = request.headers.get("Authorization", "")
        scheme, _, token = header.partition(" ")
        if scheme.lower() != "bearer" or not token.strip():
            return error("Authorization token is required", 401)
        token = token.strip().strip('"').strip("'")
        # Accept a token copied with its Bearer prefix already included.
        if token.lower().startswith("bearer "):
            token = token[7:].strip().strip('"').strip("'")
        try:
            g.current_admin = decode_access_token(token)
        except jwt.ExpiredSignatureError:
            return error("Authorization token has expired", 401)
        except jwt.InvalidTokenError:
            return error("Authorization token is invalid", 401)
        return view(*args, **kwargs)
    return wrapped
