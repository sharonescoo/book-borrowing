from datetime import date

from src.models.mongo import log_model
from src.models.postgres import senior_model
from src.utils.response_utils import error, success


def _valid_birth_date(value):
    try:
        return date.fromisoformat(value) <= date.today()
    except (TypeError, ValueError):
        return False


def list_seniors(status=None, search=None):
    return success(senior_model.list_all(status, search))


def get_senior(senior_id):
    senior = senior_model.get_by_id(senior_id)
    return success(senior) if senior else error("Senior citizen not found", 404)


def create_senior(data):
    if not _valid_birth_date(data.get("birth_date")):
        return error("birth_date must be a valid date that is not in the future")
    senior = senior_model.create(data)
    log_model.create("senior_registered", metadata={"senior_id": senior["id"]})
    return success(senior, "Senior citizen registered", 201)


def update_senior(senior_id, data):
    if "birth_date" in data and not _valid_birth_date(data["birth_date"]):
        return error("birth_date must be a valid date that is not in the future")
    senior = senior_model.update(senior_id, data)
    if not senior:
        return error("Senior citizen not found", 404)
    log_model.create("senior_updated", metadata={"senior_id": senior_id})
    return success(senior, "Senior citizen updated")


def update_status(senior_id, status, reason=None):
    if status not in {"pending", "approved", "rejected"}:
        return error("status must be pending, approved, or rejected")
    if status == "rejected" and not reason:
        return error("A rejection reason is required")
    senior = senior_model.set_status(senior_id, status, reason if status == "rejected" else None)
    if not senior:
        return error("Senior citizen not found", 404)
    log_model.create(f"senior_{status}", metadata={"senior_id": senior_id, "reason": reason})
    return success(senior, f"Registration {status}")


def delete_senior(senior_id):
    deleted = senior_model.delete(senior_id)
    if not deleted:
        return error("Senior citizen not found", 404)
    log_model.create("senior_deleted", metadata={"senior_id": senior_id})
    return success(message="Senior citizen deleted")
