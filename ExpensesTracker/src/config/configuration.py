import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URI = os.getenv("DATABASE_URI")
    DATABASE_NAME = os.getenv("DATABASE_NAME")
    FLASK_KEY = os.getenv("FLASK_KEY")
    JWT_KEY = os.getenv("JWT_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")