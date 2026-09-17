"""Book borrowing API application factory."""

import os

from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from pymongo.errors import PyMongoError
from psycopg import OperationalError

from src.utils.response_utils import error


def create_app() -> Flask:
    load_dotenv()
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "change-me"),
        JSON_SORT_KEYS=False,
    )

    from src.routes.auth_routes import auth_bp
    from src.routes.book_routes import book_bp
    from src.routes.borrow_routes import borrow_bp
    from src.routes.borrower_routes import borrower_bp
    from src.routes.document_routes import document_bp
    from src.routes.report_routes import report_bp
    from src.routes.senior_routes import senior_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(book_bp, url_prefix="/api/books")
    app.register_blueprint(borrower_bp, url_prefix="/api/borrowers")
    app.register_blueprint(borrow_bp, url_prefix="/api/borrows")
    app.register_blueprint(senior_bp, url_prefix="/api/seniors")
    app.register_blueprint(document_bp, url_prefix="/api/documents")
    app.register_blueprint(report_bp, url_prefix="/api/reports")

    @app.errorhandler(OperationalError)
    def handle_postgres_error(_exception):
        return error("PostgreSQL is unavailable. Check POSTGRES_DSN and the database service.", 503)

    @app.errorhandler(PyMongoError)
    def handle_mongo_error(_exception):
        return error("MongoDB is unavailable. Check MONGO_URI and the database service.", 503)

    @app.cli.command("init-db")
    def init_db_command():
        """Create the PostgreSQL tables used by the API."""
        from src.config.db_postgres import initialize_database
        initialize_database()
        print("Database schema initialized.")

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    @app.get("/")
    def dashboard():
        return redirect(url_for("static", filename="dashboard.html"))

    return app
