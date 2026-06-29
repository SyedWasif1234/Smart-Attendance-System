from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from PIL import Image
import numpy as np
import io

from utils.db import db
from services.auth_service import create_user , authenticate_user
from piplines.FaceRecognition import get_face_embeddings
from utils.security import create_AccessToken, create_RefreshToken, verify_token ,update_refresh_token , clear_refresh_token


router = APIRouter(
    prefix = "/auth",
    tags = ["Auth"]
)

@router.post("/register")
async def register(username: str = Form(...) , email: str = Form(...) , password: str = Form(...) , file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    image_np = np.array(image)
    
    embeddings = get_face_embeddings(image_np)
    if not embeddings:
        raise HTTPException(status_code=400, detail="No face detected in the image.")
    
    user = await create_user(username, email, password, embeddings[0].tolist())
    return {"message": "User registered successfully", "user_id": user.id}

   
@router.post("/login")
async def login( email: str = Form(...), password: str = Form(...)):
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

    except Exception as e:
        # Catch unexpected server errors, not authentication failures
        raise HTTPException(
            status_code=500,
            detail="Internal server error occurred."
        )
    

@router.post("/logout")
async def logout(user_id: str):
    await clear_refresh_token(user_id)
    return {"message": "Logged out successfully"}
