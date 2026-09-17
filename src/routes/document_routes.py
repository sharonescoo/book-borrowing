from flask import Blueprint, request

from src.controllers import document_controller
from src.middleware.auth_middleware import require_auth
from src.middleware.validate_middleware import require_json

document_bp = Blueprint("documents", __name__)

@document_bp.get("")
@require_auth
def list_documents(): return document_controller.list_documents(request.args.get("senior_id", type=int))

@document_bp.get("/<int:document_id>")
@require_auth
def get_document(document_id): return document_controller.get_document(document_id)

@document_bp.post("")
@require_auth
@require_json("senior_id", "document_type")
def create_document(): return document_controller.create_document(request.get_json())

@document_bp.patch("/<int:document_id>")
@require_auth
@require_json()
def update_document(document_id): return document_controller.update_document(document_id, request.get_json())

@document_bp.delete("/<int:document_id>")
@require_auth
def delete_document(document_id): return document_controller.delete_document(document_id)
