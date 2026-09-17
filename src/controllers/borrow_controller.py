import os
from datetime import date, datetime, timezone
from typing import Any, Mapping, cast

from src.models.mongo import fine_model, log_model
from src.models.postgres import book_model, borrow_model, borrower_model
from src.utils.response_utils import error, success


def list_borrows(): return success(borrow_model.list_all())


def create_borrow(data):
    try:
        book_id, borrower_id = int(data["book_id"]), int(data["borrower_id"])
        due_at = datetime.fromisoformat(data["due_at"].replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return error("book_id and borrower_id must be integers and due_at must be ISO-8601")
    if due_at.tzinfo is None:
        return error("due_at must include a timezone, for example 2026-10-01T12:00:00Z")
    if due_at <= datetime.now(timezone.utc):
        return error("due_at must be in the future")
    if not book_model.get_by_id(book_id): return error("Book not found", 404)
    if not borrower_model.get_by_id(borrower_id): return error("Borrower not found", 404)
    borrow = borrow_model.create(book_id, borrower_id, due_at)
    if not borrow: return error("No copies of this book are available", 409)
    borrow_data = cast(Mapping[str, Any], borrow)
    log_model.create("book_borrowed", metadata={"borrow_id": borrow_data["id"], "book_id": book_id, "borrower_id": borrower_id})
    return success(borrow_data, "Book borrowed", 201)


def return_borrow(borrow_id):
    borrow = borrow_model.return_book(borrow_id)
    if not borrow: return error("Active borrowing record not found", 404)
    borrow_data = cast(Mapping[str, Any], borrow)
    due_date = borrow_data["due_at"].date()
    overdue_days = max(0, (date.today() - due_date).days)
    if overdue_days:
        fine_model.create(borrow_id, overdue_days * float(os.getenv("FINE_PER_DAY", "5")), overdue_days)
    log_model.create("book_returned", metadata={"borrow_id": borrow_id, "days_overdue": overdue_days})
    return success({**borrow_data, "days_overdue": overdue_days}, "Book returned")
