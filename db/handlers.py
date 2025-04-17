from pymongo import MongoClient
from .schemas import Contact
from typing import Any

mongo_client = MongoClient("mongodb://localhost:27017")
collection = mongo_client["phonebook"]["contacts"]

def read(query: dict[str, Any] = {}) -> list[Contact]:
    """
    Query the database for contacts.
    """
    cursor = collection.find(query, {"_id": 0})
    return [Contact(**document) for document in cursor]
