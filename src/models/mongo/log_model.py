from datetime import datetime, timezone

from src.config.db_mongo import get_database


def create(action, actor=None, metadata=None):
    document = {"action": action, "actor": actor, "metadata": metadata or {}, "created_at": datetime.now(timezone.utc)}
    get_database().logs.insert_one(document)


def recent(limit=100):
    return list(get_database().logs.find({}, {"_id": 0}).sort("created_at", -1).limit(limit))
