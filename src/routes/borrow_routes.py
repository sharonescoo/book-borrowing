from flask import Blueprint, request

from src.controllers import borrow_controller
from src.middleware.auth_middleware import require_auth
from src.middleware.validate_middleware import require_json

borrow_bp = Blueprint("borrows", __name__)

@borrow_bp.get("")
@require_auth
def list_borrows(): return borrow_controller.list_borrows()

@borrow_bp.post("")
@require_auth
@require_json("book_id", "borrower_id", "due_at")
def create_borrow(): return borrow_controller.create_borrow(request.get_json())

@borrow_bp.post("/<int:borrow_id>/return")
@require_auth
def return_borrow(borrow_id): return borrow_controller.return_borrow(borrow_id)
