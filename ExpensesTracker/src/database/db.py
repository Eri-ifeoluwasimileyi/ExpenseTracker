from pymongo import MongoClient
from pymongo.database import Database
from src.config.configuration import Config

client: MongoClient = None
db: Database = None


def connect_db():
    global client, db
    client = MongoClient(Config.DATABASE_URI)
    db = client[Config.DATABASE_NAME]


def get_db():
    if db is None:
        raise RuntimeError("Database not initialized.")
    return db

