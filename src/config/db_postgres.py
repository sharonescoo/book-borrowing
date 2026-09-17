"""PostgreSQL connection and schema helpers."""

import os
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row


def get_dsn() -> str:
    return os.getenv("POSTGRES_DSN", "postgresql://postgres:postgres@localhost:5432/book_borrowing")


@contextmanager
def get_connection():
    with psycopg.connect(get_dsn(), row_factory=dict_row) as connection:
        yield connection


def initialize_database() -> None:
    statements = [
        """CREATE TABLE IF NOT EXISTS admins (id SERIAL PRIMARY KEY, username VARCHAR(80) UNIQUE NOT NULL, password_hash TEXT NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW())""",
        """CREATE TABLE IF NOT EXISTS borrowers (id SERIAL PRIMARY KEY, name VARCHAR(150) NOT NULL, email VARCHAR(255) UNIQUE NOT NULL, phone VARCHAR(40), created_at TIMESTAMPTZ NOT NULL DEFAULT NOW())""",
        """CREATE TABLE IF NOT EXISTS books (id SERIAL PRIMARY KEY, isbn VARCHAR(32) UNIQUE, title VARCHAR(255) NOT NULL, author VARCHAR(255) NOT NULL, total_copies INTEGER NOT NULL CHECK (total_copies >= 0), available_copies INTEGER NOT NULL CHECK (available_copies >= 0 AND available_copies <= total_copies), created_at TIMESTAMPTZ NOT NULL DEFAULT NOW())""",
        """CREATE TABLE IF NOT EXISTS borrows (id SERIAL PRIMARY KEY, book_id INTEGER NOT NULL REFERENCES books(id), borrower_id INTEGER NOT NULL REFERENCES borrowers(id), borrowed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), due_at TIMESTAMPTZ NOT NULL, returned_at TIMESTAMPTZ, created_at TIMESTAMPTZ NOT NULL DEFAULT NOW())""",
        """CREATE TABLE IF NOT EXISTS senior_citizens (id SERIAL PRIMARY KEY, first_name VARCHAR(100) NOT NULL, middle_name VARCHAR(100), last_name VARCHAR(100) NOT NULL, birth_date DATE NOT NULL, gender VARCHAR(30) NOT NULL, civil_status VARCHAR(40), address TEXT NOT NULL, barangay VARCHAR(120) NOT NULL, contact_number VARCHAR(40), email VARCHAR(255), emergency_contact VARCHAR(150), status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')), rejection_reason TEXT, registered_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW())""",
        """CREATE TABLE IF NOT EXISTS senior_documents (id SERIAL PRIMARY KEY, senior_id INTEGER NOT NULL REFERENCES senior_citizens(id) ON DELETE CASCADE, document_type VARCHAR(100) NOT NULL, reference_number VARCHAR(100), submitted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), verified BOOLEAN NOT NULL DEFAULT FALSE)""",
    ]
    with get_connection() as connection:
        with connection.cursor() as cursor:
            for statement in statements:
                cursor.execute(statement)
