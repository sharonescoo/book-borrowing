from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.db.mongo import get_logs_collection

router = APIRouter(prefix="/api/logs", tags=["logs"])


@router.get("")
async def list_logs(_=Depends(get_current_user)):
    collection = await get_logs_collection()
    logs = await collection.find({}, {"_id": 0}).sort("created_at", -1).limit(100).to_list(length=100)
    return logs
