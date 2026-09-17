from src.config.db_postgres import get_connection


def list_all(senior_id=None):
    query = "SELECT d.*, s.first_name, s.last_name FROM senior_documents d JOIN senior_citizens s ON s.id=d.senior_id"
    values = []
    if senior_id:
        query += " WHERE d.senior_id = %s"
        values.append(senior_id)
    query += " ORDER BY d.submitted_at DESC"
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute(query, values)
        return cursor.fetchall()


def get_by_id(document_id):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("SELECT * FROM senior_documents WHERE id=%s", (document_id,))
        return cursor.fetchone()


def create(data):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("INSERT INTO senior_documents (senior_id, document_type, reference_number) VALUES (%s, %s, %s) RETURNING *", (data["senior_id"], data["document_type"], data.get("reference_number")))
        return cursor.fetchone()


def update(document_id, data):
    existing = get_by_id(document_id)
    if not existing:
        return None
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("UPDATE senior_documents SET document_type=%s, reference_number=%s, verified=%s WHERE id=%s RETURNING *", (data.get("document_type", existing["document_type"]), data.get("reference_number", existing["reference_number"]), data.get("verified", existing["verified"]), document_id))
        return cursor.fetchone()


def delete(document_id):
    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM senior_documents WHERE id=%s RETURNING id", (document_id,))
        return cursor.fetchone()
