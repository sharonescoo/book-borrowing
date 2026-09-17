from flask import Blueprint, request

from src.controllers import auth_controller
from src.middleware.validate_middleware import require_json

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
@require_json("username", "password")
def register(): return auth_controller.register(request.get_json())


@auth_bp.post("/login")
@require_json("username", "password")
def login(): return auth_controller.login(request.get_json())
