"""
test_mongo_connection.py
------------------------

Verifies that the MongoDB connection using environment variables is working
and that the target database and collection are reachable.
"""

import os
from pymongo import MongoClient, errors
from dotenv import load_dotenv


def test_connection():
    """
    Loads environment variables and attempts to connect to the MongoDB cluster.
    Prints the result and lists existing documents in the target collection.

    Raises:
        ValueError: If any environment variable is missing.
    """
    load_dotenv()

    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB")
    collection_name = os.getenv("MONGO_COLLECTION")

    if not mongo_uri or not db_name or not collection_name:
        raise ValueError("Missing environment variables. Please check your .env file.")

    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")  # Quick connection test

        db = client[db_name]
        collection = db[collection_name]

        doc_count = collection.count_documents({})
        print("Successfully connected to MongoDB.")
        print(f"Database: {db_name}")
        print(f"Collection: {collection_name}")
        print(f"Documents in collection: {doc_count}")

    except errors.ServerSelectionTimeoutError as e:
        print("Failed to connect to MongoDB.")
        print("Error:", e)


if __name__ == "__main__":
    test_connection()