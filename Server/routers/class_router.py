from fastapi import APIRouter, UploadFile, File, Form, Depends, status
from services.class_service import predict_class_attendance
from utils.dependencies import require_teacher

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
    return await predict_class_attendance(subject_id, file, current_user)
