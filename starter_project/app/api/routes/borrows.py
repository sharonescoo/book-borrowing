from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.postgres import get_db
from app.models.book import Book
from app.models.borrow import Borrow
from app.models.borrower import Borrower
from app.schemas.borrows import BorrowCreate, BorrowRead
from app.services.audit_service import record_activity

router = APIRouter(prefix="/api/borrows", tags=["borrows"])


@router.get("", response_model=list[BorrowRead])
async def list_borrows(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Borrow).order_by(Borrow.borrowed_at.desc()))
    return result.scalars().all()


@router.post("", response_model=BorrowRead, status_code=status.HTTP_201_CREATED)
async def create_borrow(payload: BorrowCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    book = await db.get(Book, payload.book_id)
    borrower = await db.get(Borrower, payload.borrower_id)
    if not book or not borrower:
        raise HTTPException(status_code=404, detail="Book or borrower not found")
    if book.available_copies < 1:
        raise HTTPException(status_code=409, detail="No copies available")
    book.available_copies -= 1
    borrow = Borrow(**payload.model_dump())
    db.add(borrow)
    await db.commit()
    await db.refresh(borrow)
    await record_activity("borrow.created", current_user["username"], {"borrow_id": borrow.id})
    return borrow


@router.post("/{borrow_id}/return", response_model=BorrowRead)
async def return_borrow(borrow_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    borrow = await db.get(Borrow, borrow_id)
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    if borrow.returned_at:
        raise HTTPException(status_code=409, detail="Book has already been returned")
    borrow.returned_at = datetime.now(timezone.utc)
    book = await db.get(Book, borrow.book_id)
    if book:
        book.available_copies = min(book.total_copies, book.available_copies + 1)
    await db.commit()
    await db.refresh(borrow)
    await record_activity("borrow.returned", current_user["username"], {"borrow_id": borrow.id})
    return borrow
