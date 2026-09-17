from src.models.mongo import log_model
from src.models.postgres import senior_model
from src.utils.response_utils import success


def dashboard():
    counts = {"pending": 0, "approved": 0, "rejected": 0}
    counts.update(senior_model.count_by_status())
    return success({**counts, "total": sum(counts.values())})


def audit_logs(): return success(log_model.recent())


def registrations_by_status(status):
    return success(senior_model.list_all(status=status))
