"""MongoDB access for audit logs and fines."""

import os
from functools import lru_cache

from pymongo import MongoClient


@lru_cache(maxsize=1)
def get_database():
    client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"), serverSelectionTimeoutMS=3000)
    return client[os.getenv("MONGO_DB_NAME", "book_borrowing")]
