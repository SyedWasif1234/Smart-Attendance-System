from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from PIL import Image
import numpy as np
import io

from services.auth_service import create_user
from piplines.FaceRecognition import get_face_embeddings


router = APIRouter(
    prefix = "/auth",
    tags = ["Auth"]
)

async def register(username , email , password , file):
    
