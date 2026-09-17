from flask import Blueprint, request

from src.controllers import book_controller
from src.middleware.auth_middleware import require_auth
from src.middleware.validate_middleware import require_json

book_bp = Blueprint("books", __name__)


@book_bp.get("")
@require_auth
def list_books(): return book_controller.list_books()

@book_bp.get("/<int:book_id>")
@require_auth
def get_book(book_id): return book_controller.get_book(book_id)

@book_bp.post("")
@require_auth
@require_json("title", "author", "total_copies")
def create_book(): return book_controller.create_book(request.get_json())

@book_bp.patch("/<int:book_id>")
@require_auth
@require_json()
def update_book(book_id): return book_controller.update_book(book_id, request.get_json())

@book_bp.delete("/<int:book_id>")
@require_auth
def delete_book(book_id): return book_controller.delete_book(book_id)
