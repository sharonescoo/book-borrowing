from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes.auth import router as auth_router
from app.api.routes.books import router as books_router
from app.api.routes.borrowers import router as borrowers_router
from app.api.routes.borrows import router as borrows_router
from app.api.routes.health import router as health_router
from app.api.routes.logs import router as logs_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.ai import router as ai_router
from app.db.mongo import ping_mongo
from app.db.postgres import init_db


templates = Jinja2Templates(directory="app/templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
    except Exception as exc:
        print(f"PostgreSQL init skipped: {exc}")
    try:
        await ping_mongo()
    except Exception as exc:
        print(f"MongoDB ping skipped: {exc}")
    yield


app = FastAPI(
    title="Book Borrowing API",
    version="0.1.0",
    description="FastAPI backend for managing book borrowing, admin users, and audit logs.",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(books_router)
app.include_router(borrowers_router)
app.include_router(borrows_router)
app.include_router(logs_router)
app.include_router(dashboard_router)
app.include_router(ai_router)
