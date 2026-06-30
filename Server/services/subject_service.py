from fastapi import HTTPException, status
from utils.db import db

async def create_subject(name: str, code: str, teacher_id: str):

    try:
        Existing = await db.subject.find_first(where={"code": code})
        if Existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Subject already exists")
    
        subject = await db.subject.create(
            data={
                "name": name,
                "code": code,
                "teacherId": teacher_id
            }
        )
        return subject
    except HTTPException:
        raise  # Forward the 400 Bad Request error directly
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while creating subject: {str(e)}"
        )

async def get_all_subjects():
    try:
        return await db.subject.find_many(include={"teacher": True})
    except HTTPException:
        raise  
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error while fetching all subjects: {str(e)}"
        )