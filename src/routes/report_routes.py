from flask import Blueprint

from src.controllers import report_controller
from src.middleware.auth_middleware import require_auth

report_bp = Blueprint("reports", __name__)

@report_bp.get("/dashboard")
@require_auth
def dashboard(): return report_controller.dashboard()

@report_bp.get("/logs")
@require_auth
def audit_logs(): return report_controller.audit_logs()
