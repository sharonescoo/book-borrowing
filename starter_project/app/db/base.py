from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models.borrow import Borrow  # noqa: F401, E402
from app.models.borrower import Borrower  # noqa: F401, E402
from app.models.book import Book  # noqa: F401, E402
from app.models.user import User  # noqa: F401, E402
