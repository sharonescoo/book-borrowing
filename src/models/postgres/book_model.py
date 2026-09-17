from src.config.db_postgres import get_connection


def list_all():
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM books ORDER BY title")
        return cursor.fetchall()


def get_by_id(book_id):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        return cursor.fetchone()


def create(data):
    isbn = (data.get("isbn") or "").strip() or None
    values = (isbn, data["title"].strip(), data["author"].strip(), data["total_copies"], data["total_copies"])
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("INSERT INTO books (isbn, title, author, total_copies, available_copies) VALUES (%s, %s, %s, %s, %s) RETURNING *", values)
        return cursor.fetchone()


def update(book_id, data):
    existing = get_by_id(book_id)
    if not existing:
        return None
    total = data.get("total_copies", existing["total_copies"])
    borrowed = existing["total_copies"] - existing["available_copies"]
    if total < borrowed:
        raise ValueError("total_copies cannot be lower than copies currently borrowed")
    isbn = data.get("isbn", existing["isbn"])
    if isinstance(isbn, str):
        isbn = isbn.strip() or None
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("UPDATE books SET isbn=%s, title=%s, author=%s, total_copies=%s, available_copies=%s WHERE id=%s RETURNING *", (isbn, data.get("title", existing["title"]), data.get("author", existing["author"]), total, total - borrowed, book_id))
        return cursor.fetchone()


def delete(book_id):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM books WHERE id = %s RETURNING id", (book_id,))
        return cursor.fetchone()
