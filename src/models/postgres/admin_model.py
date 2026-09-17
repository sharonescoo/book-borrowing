from werkzeug.security import check_password_hash, generate_password_hash

from src.config.db_postgres import get_connection


def create(username, password):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("INSERT INTO admins (username, password_hash) VALUES (%s, %s) RETURNING id, username, created_at", (username, generate_password_hash(password)))
        return cursor.fetchone()


def authenticate(username, password):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT id, username, password_hash FROM admins WHERE username = %s", (username,))
        admin = cursor.fetchone()
    return admin if admin and check_password_hash(admin["password_hash"], password) else None
