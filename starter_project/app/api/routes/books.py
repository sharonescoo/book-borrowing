from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.postgres import get_db
from app.models.book import Book
from app.schemas.books import BookCreate, BookRead

router = APIRouter(prefix="/api/books", tags=["books"])


@router.get("", response_model=list[BookRead])
async def list_books(db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    result = await db.execute(select(Book).order_by(Book.title))
    return result.scalars().all()


@router.post("", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(payload: BookCreate, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    book = Book(**payload.model_dump(), available_copies=payload.total_copies)
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book


@router.get("/{book_id}", response_model=BookRead)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db), _=Depends(get_current_user)):
    book = await db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
