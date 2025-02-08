# import configparser
# from pymongo import MongoClient

# def get_db_connection():
#     # Read the configuration file
#     config = configparser.ConfigParser()
#     config.read('DB_Config.ini')

#     # Ensure 'DATABASE' section exists
#     if 'DATABASE' not in config:
#         print("Error: 'DATABASE' section not found in DB_Config.ini")
#         return None

#     mongo_uri = config['DATABASE'].get('MONGO_URI', '').strip()
#     db_name = config['DATABASE'].get('DB_NAME', '').strip()

#     if not mongo_uri or not db_name:
#         print("Error: Missing MONGO_URI or DB_NAME in DB_Config.ini")
#         return None

#     try:
#         # Connect to MongoDB
#         client = MongoClient(mongo_uri)
#         db = client[db_name]
#         print("Connected to MongoDB successfully")
#         return db
#     except Exception as e:
#         print(f"Error connecting to MongoDB: {e}")
#         return None


# if __name__ == "__main__":
#     get_db_connection()


from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = "settlement_db"

client = AsyncIOMotorClient(MONGO_URI)
database = client[DATABASE_NAME]
case_settlements_collection = database["case_settlements"]
