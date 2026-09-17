from src.config.db_postgres import get_connection


def list_all(active_only=False):
    query = "SELECT br.*, b.title AS book_title, bo.name AS borrower_name FROM borrows br JOIN books b ON b.id=br.book_id JOIN borrowers bo ON bo.id=br.borrower_id"
    if active_only:
        query += " WHERE br.returned_at IS NULL"
    query += " ORDER BY br.borrowed_at DESC"
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()


def create(book_id, borrower_id, due_at):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("UPDATE books SET available_copies=available_copies-1 WHERE id=%s AND available_copies > 0 RETURNING id", (book_id,))
        if not cursor.fetchone():
            return None
        cursor.execute("INSERT INTO borrows (book_id, borrower_id, due_at) VALUES (%s, %s, %s) RETURNING *", (book_id, borrower_id, due_at))
        return cursor.fetchone()


def return_book(borrow_id):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("UPDATE borrows SET returned_at=NOW() WHERE id=%s AND returned_at IS NULL RETURNING *", (borrow_id,))
        borrow = cursor.fetchone()
        if borrow:
            cursor.execute("UPDATE books SET available_copies=available_copies+1 WHERE id=%s", (borrow["book_id"],))
        return borrow
