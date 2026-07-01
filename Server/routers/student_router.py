from fastapi import APIRouter, Form, HTTPException, Depends, status

from services.student_service import get_all_students, get_all_students_enrolled, enroll_student
from utils.dependencies import require_teacher, require_student


student_router = APIRouter(
    prefix = "/student",
    tags = ["Student"]
)

@student_router.post("/join-class/{subject_id}", status_code=status.HTTP_201_CREATED)
async def join_class(subject_id: str, current_user = Depends(require_student)):
    print("subject id : ", subject_id)
    return await enroll_student(subject_id, current_user.id)


@student_router.get("/students")
async def read_all_students(current_user = Depends(require_teacher)):
    return await get_all_students()
    

@student_router.get("/enrolled-students/{subject_id}")
async def read_enrolled_students(subject_id: str, current_user = Depends(require_teacher)):
    return await get_all_students_enrolled(subject_id, current_user.id)
