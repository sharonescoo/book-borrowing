from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.postgres import get_db
from app.models.borrower import Borrower
from app.schemas.borrowers import BorrowerCreate, BorrowerRead

router = APIRouter(prefix="/api/borrowers", tags=["borrowers"])


@router.get("", response_model=list[BorrowerRead])
async def list_borrowers(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Borrower).order_by(Borrower.name))
    return result.scalars().all()


@router.post("", response_model=BorrowerRead, status_code=status.HTTP_201_CREATED)
async def create_borrower(payload: BorrowerCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    existing = await db.execute(select(Borrower).where(Borrower.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Borrower email already exists")
    borrower = Borrower(**payload.model_dump())
    db.add(borrower)
    await db.commit()
    await db.refresh(borrower)
    return borrower
