from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from .schemas import Contact
from typing import Any
from re import compile

mongo_client = MongoClient("mongodb://localhost:27017")
collection = mongo_client["phonebook"]["contacts"]

def read(query: dict[str, Any] = {}) -> list[Contact]:
    """
    Query the database for contacts.
    """
    cursor = collection.find(query)
    return [Contact(**document) for document in cursor]


def insert(contact: Contact) -> bool:
    """
    Insert a new contact into the database.
    """
    contact_dict = contact.model_dump(exclude={"errors"})
    contact_dict["_id"] = contact_dict.pop("id", None)

    phone_validator = compile(r"\d{3}-\d{3}-\d{4}$")
    existing_emails = collection.distinct("email")
    errors = False

    if contact.phone and not phone_validator.match(contact.phone):
        contact.errors["phone"] = "Invalid phone number format"
        errors = True
    else:
        contact.errors.pop("phone", None)

    if contact.email in existing_emails:
        contact.errors["email"] = "Email already exists"
        errors = True
    else:
        contact.errors.pop("email", None)
    
    if errors:
        return False
    
    return collection.insert_one(contact_dict).acknowledged