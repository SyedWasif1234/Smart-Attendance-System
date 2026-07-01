from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, status
from PIL import Image
import numpy as np
import io
import re

from utils.db import db
from utils.dependencies import get_current_user
from services.auth_service import create_user, authenticate_user
from pipelines.FaceRecognition import get_face_embeddings
from utils.security import create_AccessToken, create_RefreshToken, verify_token, update_refresh_token, clear_refresh_token


auth_router = APIRouter(
    prefix = "/auth",
    tags = ["Auth"]
)

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    file: UploadFile = File(...)
):
    # Input validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise HTTPException(status_code=400, detail="Invalid email format.")
    
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")
    
    if len(username.strip()) < 2:
        raise HTTPException(status_code=400, detail="Username must be at least 2 characters long.")

    # Validate image file type
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}")

    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    image_np = np.array(image)
    
    embeddings = get_face_embeddings(image_np)
    if not embeddings:
        raise HTTPException(status_code=400, detail="No face detected in the image.")
    
    user = await create_user(username, email, password, embeddings[0].tolist())
    return {"message": "User registered successfully", "user_id": user.id}

   
@auth_router.post("/login")
async def login(email: str = Form(...), password: str = Form(...)):
    try:
        user = await db.user.find_unique(where={"email": email})

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        auth_user = await authenticate_user(user.email, password)

        if not auth_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
        access_token = create_AccessToken({"sub": auth_user.id, "role": auth_user.role})
        refresh_token = create_RefreshToken({"sub": auth_user.id, "role": auth_user.role})
        await update_refresh_token(auth_user.id, refresh_token)
        return {"access_token": access_token, "refresh_token": refresh_token}

    except HTTPException:
        raise  # Forward authentication errors with correct status codes
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error occurred."
        )
    

@auth_router.post("/logout")
async def logout(current_user = Depends(get_current_user)):
    await clear_refresh_token(current_user.id)
    return {"message": "Logged out successfully"}
