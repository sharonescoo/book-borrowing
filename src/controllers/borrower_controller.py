from psycopg.errors import ForeignKeyViolation, UniqueViolation

from src.models.postgres import borrower_model
from src.utils.response_utils import error, success


def list_borrowers(): return success(borrower_model.list_all())


def get_borrower(borrower_id):
    borrower = borrower_model.get_by_id(borrower_id)
    return success(borrower) if borrower else error("Borrower not found", 404)


def create_borrower(data):
    try: borrower = borrower_model.create(data)
    except UniqueViolation: return error("Email is already in use", 409)
    return success(borrower, "Borrower created", 201)


def update_borrower(borrower_id, data):
    try: borrower = borrower_model.update(borrower_id, data)
    except UniqueViolation: return error("Email is already in use", 409)
    return success(borrower, "Borrower updated") if borrower else error("Borrower not found", 404)


def delete_borrower(borrower_id):
    try:
        deleted = borrower_model.delete(borrower_id)
    except ForeignKeyViolation:
        return error("Cannot delete a borrower with borrowing history", 409)
    return success(message="Borrower deleted") if deleted else error("Borrower not found", 404)
