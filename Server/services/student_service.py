from utils.db import db
from fastapi import HTTPException, status

async def get_student_by_id(student_id: str):
    try:
        return await db.User.find_unique(where={"id": student_id})
    except Exception as e:
        return f"Error occurred while getting student by id: {e}"

async def get_all_students():
    try:
        return await db.User.find_many(
            where={"role": "STUDENT"}
        )
    except Exception as e:
        return f"Error occurred while getting all students: {e}"
    

async def Enrollment(subject_id:str , student_id:str):
    try:
        Existing_Enrollment = await db.Enrollment.find_first(
            where = {
                "subjectId": subject_id,
                "studentId": student_id
            }
        )
        if Existing_Enrollment:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already Enrolled in this subject")
         

        return await db.Enrollment.create(
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
        enrolled_students =  await db.User.find_many(
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
            },
            select={
                "id": True,              
                "username": True,
                "email": True,
                "role": True,
                "face_embedding": True  
            }
        )

        return enrolled_students
    except Exception as e:
        return f"Error occurred while getting enrolled students: {e}"
