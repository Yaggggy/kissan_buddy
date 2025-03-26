import pyrebase
from flask import request
from face_recognition import FaceRecognition


class Login(object):

    def __init__(self):
        
        self.config = {
            "apiKey": "your-api-key",
            "authDomain": "your-auth-domain",
            "databaseURL": "your-database-url",
            "projectId": "your-project-id",
            "storageBucket": "your-storage-bucket",
            "messagingSenderId": "your-messaging-sender-id",
            "appId": "your-app-id"
        }


        self.firebase = pyrebase.initialize_app(self.config)

        self.auth = self.firebase.auth()
        self.face_recognition = FaceRecognition()

    def kisan_login(self):
        email = request.form['email']
        password = request.form['password']
        face_image = request.files['face_image']

        try:
            # Save the face image temporarily
            temp_path = "static/temp/face.jpg"
            face_image.save(temp_path)

            # Verify face
            success, message = self.face_recognition.verify_face(temp_path)
            if not success:
                return 'failed', None

            # Authenticate with Firebase
            user = self.auth.sign_in_with_email_and_password(email, password)
            return 'successful', email
        except Exception as e:
            return 'failed', None

    def register_face(self, user_id, face_image):
        temp_path = "static/temp/face.jpg"
        face_image.save(temp_path)
        success, message = self.face_recognition.register_face(temp_path, user_id)
        return success, message