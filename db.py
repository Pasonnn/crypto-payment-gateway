import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class Database:
    _instance = None

    # Singleton pattern
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            uri = os.getenv("DATABASE_URI")
            db_name = os.getenv("DATABASE_NAME")
            cls._instance.client = MongoClient(uri)
            cls._instance.db = cls._instance.client[db_name]
            print(f"<console> Connected to MongoDB: {db_name}")
        return cls._instance

    # Get collection from database
    @staticmethod
    def get_collection(collection_name):
        if Database._instance is None:
            Database()
        return Database._instance.db[collection_name]