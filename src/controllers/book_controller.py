from psycopg.errors import ForeignKeyViolation, UniqueViolation

from src.models.mongo import log_model
from src.models.postgres import book_model
from src.utils.response_utils import error, success


def list_books(): return success(book_model.list_all())


def get_book(book_id):
    book = book_model.get_by_id(book_id)
    return success(book) if book else error("Book not found", 404)


def create_book(data):
    try:
        data["total_copies"] = int(data["total_copies"])
        if data["total_copies"] < 0: raise ValueError
        book = book_model.create(data)
    except ValueError:
        return error("total_copies must be a non-negative integer")
    except UniqueViolation:
        return error("ISBN is already in use", 409)
    log_model.create("book_created", metadata={"book_id": book["id"]})
    return success(book, "Book created", 201)


def update_book(book_id, data):
    try:
        if "total_copies" in data:
            if isinstance(data["total_copies"], bool):
                raise ValueError
            data["total_copies"] = int(data["total_copies"])
            if data["total_copies"] < 0:
                raise ValueError
        book = book_model.update(book_id, data)
    except ValueError as exc:
        message = str(exc) if str(exc) == "total_copies cannot be lower than copies currently borrowed" else "total_copies must be a non-negative integer"
        return error(message)
    except UniqueViolation:
        return error("ISBN is already in use", 409)
    return success(book, "Book updated") if book else error("Book not found", 404)


def delete_book(book_id):
    try:
        deleted = book_model.delete(book_id)
    except ForeignKeyViolation:
        return error("Cannot delete a book with borrowing history", 409)
    return success(message="Book deleted") if deleted else error("Book not found", 404)
