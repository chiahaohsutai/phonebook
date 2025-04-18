import asyncio
import json
import logging
import pathlib
from os import getcwd
from uuid import uuid4

from pymongo import AsyncMongoClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mongo_conn_string = "mongodb://localhost:27017"
mongo_client = AsyncMongoClient(mongo_conn_string)

db = mongo_client["phonebook"]
collection = db["contacts"]


async def populate():
    if await collection.count_documents({}) == 0:
        file_path = pathlib.Path(getcwd()) / "data" / "contacts.json"
        with open(file_path, "r") as file:
            data = json.load(file)
        
        for item in data:
            item["_id"] = str(uuid4())
            item.pop("errors", None)
            item.pop("id", None)

        result = await collection.insert_many(data)

        if result.acknowledged:
            await collection.create_index({ "email": 1 }, unique=True)
            logger.info("Data inserted successfully.")
        else:
            logger.error("Failed to insert data.")

        num_docs = len(result.inserted_ids)
        logger.info(f"Inserted {num_docs} documents into the collection.")
        logger.info("Data inserted successfully.")
    else:
        logger.info("Collection already populated.")


if __name__ == "__main__":
    asyncio.run(populate())
