from flask import Blueprint, request

from src.controllers import borrower_controller
from src.middleware.auth_middleware import require_auth
from src.middleware.validate_middleware import require_json

borrower_bp = Blueprint("borrowers", __name__)

@borrower_bp.get("")
@require_auth
def list_borrowers(): return borrower_controller.list_borrowers()

@borrower_bp.get("/<int:borrower_id>")
@require_auth
def get_borrower(borrower_id): return borrower_controller.get_borrower(borrower_id)

@borrower_bp.post("")
@require_auth
@require_json("name", "email")
def create_borrower(): return borrower_controller.create_borrower(request.get_json())

@borrower_bp.patch("/<int:borrower_id>")
@require_auth
@require_json()
def update_borrower(borrower_id): return borrower_controller.update_borrower(borrower_id, request.get_json())

@borrower_bp.delete("/<int:borrower_id>")
@require_auth
def delete_borrower(borrower_id): return borrower_controller.delete_borrower(borrower_id)
