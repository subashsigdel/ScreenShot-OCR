from pymongo import MongoClient
from datetime import datetime
from db_connection import client

db = client["ocr_Screenshot_db"]

# Example: Get all users
for user in db["users"].find():
    print(user)

# Example: Get all OCR results for a specific user
user_id = "subash"
for ocr in db["ocr_results"].find({"user_id": user_id}):
    print(ocr)
