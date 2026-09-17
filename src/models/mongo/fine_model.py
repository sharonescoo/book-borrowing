from datetime import datetime, timezone

from src.config.db_mongo import get_database


def create(borrow_id, amount, days_overdue):
    document = {"borrow_id": borrow_id, "amount": amount, "days_overdue": days_overdue, "paid": False, "created_at": datetime.now(timezone.utc)}
    get_database().fines.update_one({"borrow_id": borrow_id}, {"$setOnInsert": document}, upsert=True)


def list_all():
    return list(get_database().fines.find({}, {"_id": 0}).sort("created_at", -1))
