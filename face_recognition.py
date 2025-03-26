import cv2
import face_recognition
import numpy as np
import os
from PIL import Image

class FaceRecognition:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    def load_known_faces(self):
        # Load known faces from a directory
        faces_dir = "static/known_faces"
        if not os.path.exists(faces_dir):
            os.makedirs(faces_dir)
            return

        for filename in os.listdir(faces_dir):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(faces_dir, filename)
                image = face_recognition.load_image_file(path)
                face_encoding = face_recognition.face_encodings(image)[0]
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(os.path.splitext(filename)[0])

    def verify_face(self, image_path):
        try:
            # Load and process the image
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            if not face_encodings:
                return False, "No face detected"

            # Compare with known faces
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                    return True, name

            return False, "Face not recognized"
        except Exception as e:
            return False, str(e)

    def register_face(self, image_path, user_id):
        try:
            # Load and process the image
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            if not face_encodings:
                return False, "No face detected"

            # Save the face encoding
            face_encoding = face_encodings[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(user_id)

            # Save the image
            faces_dir = "static/known_faces"
            if not os.path.exists(faces_dir):
                os.makedirs(faces_dir)
            
            image_path = os.path.join(faces_dir, f"{user_id}.jpg")
            Image.fromarray(image).save(image_path)

            return True, "Face registered successfully"
        except Exception as e:
            return False, str(e) 