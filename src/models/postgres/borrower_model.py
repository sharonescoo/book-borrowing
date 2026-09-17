from src.config.db_postgres import get_connection


def list_all():
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM borrowers ORDER BY name")
        return cursor.fetchall()


def get_by_id(borrower_id):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM borrowers WHERE id = %s", (borrower_id,))
        return cursor.fetchone()


def create(data):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("INSERT INTO borrowers (name, email, phone) VALUES (%s, %s, %s) RETURNING *", (data["name"], data["email"], data.get("phone")))
        return cursor.fetchone()


def update(borrower_id, data):
    existing = get_by_id(borrower_id)
    if not existing:
        return None
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("UPDATE borrowers SET name=%s, email=%s, phone=%s WHERE id=%s RETURNING *", (data.get("name", existing["name"]), data.get("email", existing["email"]), data.get("phone", existing["phone"]), borrower_id))
        return cursor.fetchone()


def delete(borrower_id):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM borrowers WHERE id = %s RETURNING id", (borrower_id,))
        return cursor.fetchone()
