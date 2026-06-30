from utils.db import db
from fastapi import status, UploadFile, HTTPException
from PIL import Image
import numpy as np
import io
from piplines.FaceRecognition import predict_attendance

async def save_attendance_records(subject_id: str, detected_students: dict, all_students: list):
    records = []
   
    for student_id in all_students:
        is_present = detected_students.get(student_id, False)
        records.append({
            "subjectId": subject_id,
            "studentId": student_id,
            "status": "PRESENT" if is_present else "ABSENT"
        })
       
    if records:
        # FIX: Capitalized 'Attendance' to match your Prisma schema
        await db.Attendance.create_many(data=records)
       
    return records

async def Predict_Attendance(subject_id: str, file: UploadFile, current_user):
    try:
        contents = await file.read()
        class_image = Image.open(io.BytesIO(contents)).convert('RGB')
        class_image_np = np.array(class_image)
       
        if class_image_np.size == 0:
            raise HTTPException(status_code=400, detail="Invalid image uploaded.")
     
        # Call the pipeline using the parameters passed from the route
        detected_students, all_students, _ = await predict_attendance(
            class_image_np,
            subject_id=subject_id,
            teacher_id=current_user.id
        )

        saved_records = await save_attendance_records(
            subject_id=subject_id,
            detected_students=detected_students,
            all_students=all_students
        )

        return {
            "message": "Attendance calculated and saved successfully",
            "total_enrolled": len(all_students),
            "total_present": len(detected_students),
            "records_saved": len(saved_records)
        }
    except HTTPException:
        raise  
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error occurred while getting attendance: {str(e)}"
        )
