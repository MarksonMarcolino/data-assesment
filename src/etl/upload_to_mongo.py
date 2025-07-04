"""
Module: upload_to_mongo
------------------------
Provides functionality to upload a pandas DataFrame to a MongoDB Atlas collection.

Usage:
    from etl.upload_to_mongo import upload_dataframe_to_mongo
    upload_dataframe_to_mongo(df)
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv


def upload_dataframe_to_mongo(df, drop_existing=True):
    """
    Uploads a pandas DataFrame to a MongoDB collection.

    Credentials and configuration are expected in a `.env` file:
        MONGO_URI=mongodb+srv://<user>:<password>@<cluster>/?retryWrites=true&w=majority
        MONGO_DB=your_database
        MONGO_COLLECTION=your_collection

    Args:
        df (pd.DataFrame): The DataFrame to upload. It should be pre-cleaned (no NaT, NaN).
        drop_existing (bool): If True, clears the existing collection before inserting.
    
    Raises:
        ValueError: If environment variables are missing.
    """
    # Load environment variables
    load_dotenv()

    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB")
    collection_name = os.getenv("MONGO_COLLECTION")

    if not mongo_uri or not db_name or not collection_name:
        raise ValueError("Missing MongoDB credentials or config in .env file.")

    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Optionally drop existing documents
    if drop_existing:
        collection.delete_many({})

    # Convert to records and insert
    records = df.to_dict("records")
    if records:
        collection.insert_many(records)
        print(f"Uploaded {len(records)} records to MongoDB → {db_name}.{collection_name}")
    else:
        print("No records to upload.")