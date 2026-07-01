from fastapi import APIRouter, Form, HTTPException, Depends, status
from services.subject_service import create_subject, get_all_subjects
from utils.dependencies import require_teacher, get_current_user

subject_router = APIRouter(
    prefix = "/subject",
    tags = ["Subject"]
)

@subject_router.post("/create-subject", status_code=status.HTTP_201_CREATED)
async def create(name: str = Form(...), code: str = Form(...), current_user = Depends(require_teacher)):
    print(f"""Current User: {current_user.username}""")
    return await create_subject(name, code, current_user.id)

@subject_router.get("/subjects")
async def read_all_subjects(current_user = Depends(get_current_user)):
    return await get_all_subjects()