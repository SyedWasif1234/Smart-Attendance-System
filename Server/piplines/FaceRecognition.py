import dlib
import numnpy as np
import face_recognition_models
form sklearn.svm import SVC
from functools import lru_cache # FastAPI's way of caching heavy models!

# Call this whenever you retrain the model or update the underlying files
def refresh_models():
    # Force the dlib models to be reloaded from disk
    load_dlib_models.cache_clear()
    print("Cache cleared! Models will reload on next request.")

# we will only load it once because it is heavy
@lru_cache(maxsize=1)
def load_dlib_models():
    detector = dlib.get_frontal_face_detector() # detect faces

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
        face_descriptor = face_recognizer.compute_face_descriptor(image_np, shape,1)
        face_encodings.append(np.array(face_descriptor))

    return face_encodings


def get_trained_model():
    X = []
    y = []

    # students = get_all_students()  - commented out because not yet build this 

    if not students:
        return None
    
    for student in students:

        embedding = student.get('face_embedding')

        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))


    if len(X) == 0:
        return 0
    
    clf = SVC(kernel='linear', probability=True , class_weight='balanced')

    try:
        clf.fit(X, y)
    except:
        return None

    return {'clf':clf , 'X':X, 'y':y}

def train_classifiers():
    refresh_models()
    model_data = get_trained_model()
    return bool(model_data)

def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)

    detected_students = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_students , [] , len(encodings)
    
    clf = model_data['clf']
    X_train = model_data['X']
    Y_train = model_data['y']

    all_students = sorted(list(set(Y_train)))

    for encoding in encodings:
        if len(all_students) >= 2:
            predicted_id = int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])
            

        student_embedding = X_train(Y_train.index(predicted_id))

        best_match_score = np.linalg.norm(student_embedding - encoding)

        resemblance_threshold = 0.6 # means distance must be less than 0.6

        if best_match_score < resemblance_threshold:
            detected_students[predicted_id] = True

    return detected_students , all_students , len(encodings)



    

