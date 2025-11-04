from fastapi import FastAPI, UploadFile, File, HTTPException,Form
from fastapi.responses import FileResponse, JSONResponse
from datetime import datetime
from Modules.Database.db_connection import client
from Modules.ImageToText import extract_text
import os

app = FastAPI()

# initialize database
db = client["ocr_Screenshot_db"]
ocr_col = db["ocr_results"]
users_col = db["users"]

# Folder to save images
IMAGE_FOLDER = "Images/Saved_images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)


@app.post("/register/")
async def register_user(username: str = Form(...)):
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")

    # Check if user exists
    if users_col.find_one({"username": username}):
        return JSONResponse({"message": "User already exists", "username": username})

    # Create new user
    users_col.insert_one({
        "username": username,
        "created_at": datetime.now()
    })

    return JSONResponse({"message": "User registered", "username": username})

#API: Upload an image
@app.post("/upload/")
async def upload_image(
    file: UploadFile = File(...),
    username: str = Form(...)
):
    # Check if username exists
    if not users_col.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="User not registered")

    # Predictable filename
    unique_filename = f"{username}_{file.filename}"
    file_path = os.path.join("Images/Saved_images", unique_filename)

    # Save image
    with open(file_path, "wb") as buffer:
        import shutil
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    text = extract_text(file_path)

    # Store in MongoDB
    ocr_col.insert_one({
        "user_id": username,
        "filename": unique_filename,
        "text": text,
        "uploaded_at": datetime.now()
    })

    return {"username": username, "filename": unique_filename, "text": text}

# API: Get image by filename
@app.get("/image/{filename}")
async def get_image(filename: str):
    file_path = os.path.join(IMAGE_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

# API: Get extracted text by filename
@app.get("/text/{filename}")
async def get_text(filename: str):
    record = ocr_col.find_one({"filename": filename})
    if not record:
        raise HTTPException(status_code=404, detail="OCR result not found")
    return JSONResponse({"filename": record["filename"], "text": record["text"]})
