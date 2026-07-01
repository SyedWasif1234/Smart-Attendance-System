import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
from functools import lru_cache

from services.student_service import get_all_students_enrolled

# We will only load it once because it is heavy
@lru_cache(maxsize=1)
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()
    shape_predictor = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    face_recognizer = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector, shape_predictor, face_recognizer

def get_face_embeddings(image_np):
    detector, shape_predictor, face_recognizer = load_dlib_models()
    faces = detector(image_np, 1)
    face_encodings = []

    for face in faces:
        shape = shape_predictor(image_np, face)
        face_descriptor = face_recognizer.compute_face_descriptor(image_np, shape, 1)
        face_encodings.append(np.array(face_descriptor))

    return face_encodings


async def get_trained_model(subject_id: str, teacher_id: str):
    X = []
    y = []

    students = await get_all_students_enrolled(subject_id, teacher_id)  

    if not students:
        return None
    
    for student in students:
        #  Change dot-notation to dictionary lookups
        embedding = student.get("face_embedding")
        student_id = student.get("id")
        
        if embedding:
            X.append(np.array(embedding))
            y.append(student_id)

    if len(X) == 0:
        return None

    # Need at least 2 unique classes for SVC to train meaningfully
    unique_classes = set(y)
    if len(unique_classes) < 2:
        # With only 1 student, skip SVC — return data for direct matching
        return {'clf': None, 'X': X, 'y': y}
    
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')
    try:
        clf.fit(X, y)
    except ValueError as e:
        # Log the actual error instead of silently swallowing it
        print(f"SVC training failed: {e}")
        return None

    return {'clf': clf, 'X': X, 'y': y}


async def predict_attendance(class_image_np, subject_id: str, teacher_id: str):
    encodings = get_face_embeddings(class_image_np)
    detected_students = {}

    model_data = await get_trained_model(subject_id, teacher_id)

    if not model_data:
        return detected_students, [], len(encodings)
    
    clf = model_data['clf']
    X_train = model_data['X']
    Y_train = model_data['y']

    all_students = sorted(list(set(Y_train)))

    for encoding in encodings:
        if clf is not None and len(all_students) >= 2:
            predicted_id = str(clf.predict([encoding])[0])
        else:
            # Single student — use direct distance matching
            predicted_id = str(all_students[0])
            
        student_embedding = X_train[Y_train.index(predicted_id)]
        best_match_score = np.linalg.norm(student_embedding - encoding)

        resemblance_threshold = 0.6 
        if best_match_score < resemblance_threshold:
            detected_students[predicted_id] = True

    return detected_students, all_students, len(encodings)