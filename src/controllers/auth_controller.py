from psycopg.errors import UniqueViolation

from src.models.postgres import admin_model
from src.utils.jwt_utils import create_access_token
from src.utils.response_utils import error, success


def register(data):
    try:
        admin = admin_model.create(data["username"], data["password"])
    except UniqueViolation:
        return error("Username is already in use", 409)
    return success({"admin": admin, "token": create_access_token(admin)}, "Admin registered", 201)


def login(data):
    admin = admin_model.authenticate(data["username"], data["password"])
    if not admin:
        return error("Invalid username or password", 401)
    return success({"token": create_access_token(admin), "admin": {"id": admin["id"], "username": admin["username"]}}, "Logged in")
