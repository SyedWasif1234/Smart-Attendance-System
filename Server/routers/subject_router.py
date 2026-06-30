from fastapi import APIRouter,  Form, HTTPException , Depends , status
from services.subject_service import create_subject , get_all_subjects
from utils.dependencies import require_teacher

subject_router = APIRouter(
    prefix = "/subject",
    tags = ["Subject"]
)

@subject_router.post("/create-subject")
async def Create(name: str = Form(...), code: str = Form(...), current_user = Depends(require_teacher)):
    try:
        return await create_subject(name , code ,current_user.id)
    except Exception as e:
        return f"Error occurred while creating subject: {e}"

@subject_router.get("/subjects")
async def read_all_subjects():
    try:
        return await get_all_subjects()
    except Exception as e:
        return f"Error occurred while getting all subjects: {e}"