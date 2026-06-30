from fastapi import APIRouter, UploadFile, File, Form, Depends, status
from services.class_service import Predict_Attendance
from utils.dependencies import require_teacher # Double check your import path

class_router = APIRouter(
    prefix="/class",
    tags=["Class"]
)

@class_router.post("/take-attendance", status_code=status.HTTP_201_CREATED)
async def take_attendance(
    subject_id: str = Form(...), 
    file: UploadFile = File(...), 
    current_user = Depends(require_teacher)
):
    return await Predict_Attendance(subject_id, file, current_user)
