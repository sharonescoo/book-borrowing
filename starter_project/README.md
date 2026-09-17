# Book Borrowing API

A FastAPI backend for administrator authentication, book inventory, borrowers, borrowing transactions, and MongoDB activity logs using:
- PostgreSQL via SQLAlchemy AsyncEngine
- MongoDB Atlas via Motor
- Jinja2 backend console
- Tailwind CSS via CDN

## Setup

Use Python 3.12 or newer on Windows. The dependency ranges are intentionally current enough to use wheels on Python 3.14.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Run locally

```bash
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000` and its OpenAPI UI at `/docs`.

## Database workflow

```bash
alembic upgrade head
```

PostgreSQL stores users, books, borrowers, and borrows. MongoDB stores administrator activity logs in `MONGO_LOGS_COLLECTION`.

## Vercel deployment

```bash
vercel
vercel --prod
```

## Notes

- Add your environment variables in `.env`
- PostgreSQL is for transactional data
- MongoDB is for administrator activity logs and flexible records
- UI is server-rendered Jinja2 and styled with Tailwind CDN
