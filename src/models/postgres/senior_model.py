from src.config.db_postgres import get_connection


FIELDS = ("first_name", "middle_name", "last_name", "birth_date", "gender", "civil_status", "address", "barangay", "contact_number", "email", "emergency_contact")


def list_all(status=None, search=None):
    query = "SELECT * FROM senior_citizens"
    clauses, values = [], []
    if status:
        clauses.append("status = %s")
        values.append(status)
    if search:
        clauses.append("(first_name ILIKE %s OR last_name ILIKE %s OR barangay ILIKE %s OR contact_number ILIKE %s)")
        values.extend([f"%{search}%"] * 4)
    if clauses:
        query += " WHERE " + " AND ".join(clauses)
    query += " ORDER BY registered_at DESC"
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(query, values)
        return cursor.fetchall()


def get_by_id(senior_id):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM senior_citizens WHERE id = %s", (senior_id,))
        return cursor.fetchone()


def create(data):
    columns = ", ".join(FIELDS)
    placeholders = ", ".join(["%s"] * len(FIELDS))
    values = [data.get(field) for field in FIELDS]
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(f"INSERT INTO senior_citizens ({columns}) VALUES ({placeholders}) RETURNING *", values)
        return cursor.fetchone()


def update(senior_id, data):
    allowed = {key: value for key, value in data.items() if key in FIELDS}
    if not allowed:
        return get_by_id(senior_id)
    assignments = ", ".join(f"{field} = %s" for field in allowed)
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(f"UPDATE senior_citizens SET {assignments}, updated_at = NOW() WHERE id = %s RETURNING *", [*allowed.values(), senior_id])
        return cursor.fetchone()


def set_status(senior_id, status, rejection_reason=None):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("UPDATE senior_citizens SET status=%s, rejection_reason=%s, updated_at=NOW() WHERE id=%s RETURNING *", (status, rejection_reason, senior_id))
        return cursor.fetchone()


def delete(senior_id):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM senior_citizens WHERE id = %s RETURNING id", (senior_id,))
        return cursor.fetchone()


def count_by_status():
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT status, COUNT(*) AS count FROM senior_citizens GROUP BY status")
        return {row["status"]: row["count"] for row in cursor.fetchall()}
