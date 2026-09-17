from flask import Blueprint, request

from src.controllers import senior_controller
from src.middleware.auth_middleware import require_auth
from src.middleware.validate_middleware import require_json

senior_bp = Blueprint("seniors", __name__)

@senior_bp.get("")
@require_auth
def list_seniors(): return senior_controller.list_seniors(request.args.get("status"), request.args.get("search"))

@senior_bp.get("/search")
@require_auth
def search_seniors(): return senior_controller.list_seniors(search=request.args.get("q", ""))

@senior_bp.get("/pending")
@require_auth
def pending_seniors(): return senior_controller.list_seniors(status="pending")

@senior_bp.get("/<int:senior_id>")
@require_auth
def get_senior(senior_id): return senior_controller.get_senior(senior_id)

@senior_bp.post("")
@require_auth
@require_json("first_name", "last_name", "birth_date", "gender", "address", "barangay")
def create_senior(): return senior_controller.create_senior(request.get_json())

@senior_bp.patch("/<int:senior_id>")
@require_auth
@require_json()
def update_senior(senior_id): return senior_controller.update_senior(senior_id, request.get_json())

@senior_bp.patch("/<int:senior_id>/status")
@require_auth
@require_json("status")
def set_status(senior_id):
    data = request.get_json()
    return senior_controller.update_status(senior_id, data["status"], data.get("rejection_reason"))

@senior_bp.patch("/<int:senior_id>/approve")
@require_auth
def approve(senior_id): return senior_controller.update_status(senior_id, "approved")

@senior_bp.patch("/<int:senior_id>/reject")
@require_auth
@require_json("rejection_reason")
def reject(senior_id): return senior_controller.update_status(senior_id, "rejected", request.get_json()["rejection_reason"])

@senior_bp.delete("/<int:senior_id>")
@require_auth
def delete_senior(senior_id): return senior_controller.delete_senior(senior_id)
