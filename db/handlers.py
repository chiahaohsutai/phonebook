from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from .schemas import Contact
from typing import Any
from re import compile

mongo_client = MongoClient("mongodb://localhost:27017")
collection = mongo_client["phonebook"]["contacts"]


def read(*steps: dict[str, Any]) -> list[Contact]:
    """
    Query the database for contacts.
    """
    cursor = collection.aggregate(list(steps))
    return [Contact(**document) for document in cursor]


def count() -> int:
    """
    Count the number of contacts in the database.
    """
    return collection.count_documents({})


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


def update(contact: Contact) -> bool:
    """
    Update an existing contact in the database.
    """
    contact_dict = contact.model_dump(exclude={"errors"})
    contact_dict["_id"] = contact_dict.pop("id", None)

    phone_validator = compile(r"\d{3}-\d{3}-\d{4}$")
    errors = False

    if contact.phone and not phone_validator.match(contact.phone):
        contact.errors["phone"] = "Invalid phone number format"
        errors = True
    else:
        contact.errors.pop("phone", None)

    if errors:
        return False

    try:
        result = collection.update_one({"_id": contact.id}, {"$set": contact_dict})
        return result.modified_count > 0
    except DuplicateKeyError:
        contact.errors["email"] = "Email already exists"
        return False


def delete(contact_id: str | list[str]) -> bool:
    """
    Delete a contact from the database.
    """
    if not isinstance(contact_id, list):
        contact_id = [contact_id]

    result = collection.delete_many({"_id": {"$in": contact_id}})
    return result.deleted_count > 0
