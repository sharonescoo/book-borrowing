"""Create initial book borrowing tables.

Revision ID: 0001_initial
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("admin_users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("username", sa.String(80), nullable=False, unique=True), sa.Column("email", sa.String(255), nullable=True, unique=True), sa.Column("password_hash", sa.String(255), nullable=False), sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_table("books", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("isbn", sa.String(32), unique=True), sa.Column("title", sa.String(255), nullable=False), sa.Column("author", sa.String(255), nullable=False), sa.Column("total_copies", sa.Integer(), nullable=False), sa.Column("available_copies", sa.Integer(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_table("borrowers", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(150), nullable=False), sa.Column("email", sa.String(255), nullable=False, unique=True), sa.Column("phone", sa.String(40)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_table("borrows", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("book_id", sa.Integer(), sa.ForeignKey("books.id"), nullable=False), sa.Column("borrower_id", sa.Integer(), sa.ForeignKey("borrowers.id"), nullable=False), sa.Column("borrowed_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.Column("due_at", sa.DateTime(timezone=True), nullable=False), sa.Column("returned_at", sa.DateTime(timezone=True)), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))


def downgrade() -> None:
    op.drop_table("borrows")
    op.drop_table("borrowers")
    op.drop_table("books")
    op.drop_table("admin_users")
