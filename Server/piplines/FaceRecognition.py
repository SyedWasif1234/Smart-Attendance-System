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

# FIX 1: We must pass subject_id and teacher_id to only load students in THIS class
async def get_trained_model(subject_id: str, teacher_id: str):
    X = []
    y = []

    # FIX 2: We must await the database call and pass the parameters
    students = await get_all_students_enrolled(subject_id, teacher_id)  

    if not students:
        return None
    
    for student in students:
        # FIX 3: Use Prisma object syntax (.face_embedding), not dictionary .get()
        embedding = student.face_embedding
        if embedding:
            X.append(np.array(embedding))
            y.append(student.id)

    if len(X) == 0:
        return None
    
    clf = SVC(kernel='linear', probability=True, class_weight='balanced')
    try:
        clf.fit(X, y)
    except:
        return None

    return {'clf': clf, 'X': X, 'y': y}


# FIX 4: This function must be async because it calls get_trained_model (which talks to the DB)
async def predict_attendance(class_image_np, subject_id: str, teacher_id: str):
    encodings = get_face_embeddings(class_image_np)
    detected_students = {}

    # We must await the async model builder
    model_data = await get_trained_model(subject_id, teacher_id)

    if not model_data:
        return detected_students, [], len(encodings)
    
    clf = model_data['clf']
    X_train = model_data['X']
    Y_train = model_data['y']

    all_students = sorted(list(set(Y_train)))

    for encoding in encodings:
        if len(all_students) >= 2:
            # FIX 5: Your IDs are UUID Strings, NOT integers! int() will crash. Use str()
            predicted_id = str(clf.predict([encoding])[0])
        else:
            predicted_id = str(all_students[0])
            
        # FIX 6: Use square brackets [] for list indexing, NOT parentheses ()
        student_embedding = X_train[Y_train.index(predicted_id)]
        best_match_score = np.linalg.norm(student_embedding - encoding)

        resemblance_threshold = 0.6 
        if best_match_score < resemblance_threshold:
            detected_students[predicted_id] = True

    return detected_students, all_students, len(encodings)