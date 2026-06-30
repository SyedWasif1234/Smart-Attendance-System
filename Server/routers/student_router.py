from fastapi import APIRouter,  Form, HTTPException , Depends , status

from services.student_service import get_student_by_id, get_all_students, get_all_students_enrolled , Enrollment
from utils.dependencies import require_teacher , require_student


student_router = APIRouter(
    prefix = "/student",
    tags = ["Student"]
)

@student_router.post("/join-class/{subject_id}")
async def join_class(subject_id: str, current_user = Depends(require_student)):
    try:
        return await Enrollment(subject_id, current_user.id)
    except Exception as e:
        return f"Error occurred while joining class: {e}"



@student_router.get("/students")
async def read_all_students(current_user = Depends(require_teacher)):
    try:
        return await get_all_students()
    except Exception as e:
        return f"Error occurred while getting all students: {e}"
    

@student_router.get("/Enrolled-students/{subject_id}")
async def read_enrolled_students(subject_id: str, current_user = Depends(require_teacher)):
    try:
        return await get_all_students_enrolled(subject_id, current_user.id)
    except Exception as e:
        return f"Error occurred while getting enrolled students: {e}"

