from utils.db import db
from fastapi import HTTPException, status

async def get_student_by_id(student_id: str):
    try:
        student = await db.user.find_unique(where={"id": student_id})
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        return student
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while getting student by id: {str(e)}"
        )

async def get_all_students():
    try:
        return await db.user.find_many(
            where={"role": "STUDENT"},
            select={
                "id": True,
                "username": True,
                "email": True,
                "role": True,
                "createdAt": True,
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while getting all students: {str(e)}"
        )
    

async def enroll_student(subject_id: str, student_id: str):
    try:
        existing_enrollment = await db.enrollment.find_first(
            where = {
                "subjectId": subject_id,
                "studentId": student_id
            }
        )
        if existing_enrollment:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already Enrolled in this subject")
         

        return await db.enrollment.create(
            data={
                "subjectId": subject_id,
                "studentId": student_id
                }
            )
    
    except HTTPException:
        raise  # Forward the 400 Bad Request error directly
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while creating enrollment: {str(e)}"
        )


async def get_all_students_enrolled(subject_id: str, teacher_id: str):
    try:

        users = await db.user.find_many(
            where={
                "role": "STUDENT",
                "enrollments": {
                    "some": {
                        "subjectId": subject_id,
                        "subject": {
                            "teacherId": teacher_id
                        }
                    }
                }
            }
        )

        enrolled_students = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "face_embedding": user.face_embedding
            }
            for user in users
        ]

        return enrolled_students
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while getting enrolled students: {str(e)}"
        )
