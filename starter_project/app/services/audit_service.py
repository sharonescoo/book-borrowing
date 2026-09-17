from datetime import datetime, timezone

from app.db.mongo import get_logs_collection


async def record_activity(action: str, username: str | None = None, details: dict | None = None) -> None:
    try:
        collection = await get_logs_collection()
        await collection.insert_one({
            "action": action,
            "username": username,
            "details": details or {},
            "created_at": datetime.now(timezone.utc),
        })
    except Exception:
        # Audit storage must not turn a successful business transaction into a 5xx.
        return
