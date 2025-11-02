from pymongo import MongoClient
from datetime import datetime
from db_connection import client
# Create a new database (it will be created when you first write to it)
db = client["ocr_Screenshot_db"]

# Create collections (tables in SQL terms)
users_col = db["users"]
ocr_col = db["ocr_results"]

# Optional: Insert a dummy document to actually create the database
users_col.insert_one({
    "username": "subash",
    "email": "subash@example.com",
    "password_hash": "1234",
    "created_at":datetime.now()
})


ocr_col.insert_one({
    "user_id": "subash_id",
    "filename": "screenshot_123.png",
    "text": "Extracted text from the image",
    "uploaded_at": datetime.now()
})


print("Database and collections created successfully!")
