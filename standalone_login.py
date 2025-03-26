import cv2
import face_recognition
import numpy as np
import os
from PIL import Image
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class FaceLoginSystem:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()
        
        # Create GUI window
        self.window = tk.Tk()
        self.window.title("Face Recognition Login System")
        self.window.geometry("400x300")
        
        # Create buttons
        self.register_btn = tk.Button(self.window, text="Register New User", command=self.register_user)
        self.register_btn.pack(pady=20)
        
        self.login_btn = tk.Button(self.window, text="Login", command=self.login)
        self.login_btn.pack(pady=20)
        
        # Create label for status
        self.status_label = tk.Label(self.window, text="")
        self.status_label.pack(pady=20)
        
        # Initialize camera
        self.cap = None
        
    def load_known_faces(self):
        faces_dir = "known_faces"
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
    
    def capture_image(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
        
        ret, frame = self.cap.read()
        if ret:
            # Convert frame to RGB
            rgb_frame = frame[:, :, ::-1]
            return rgb_frame
        return None
    
    def register_user(self):
        user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Capture image
        frame = self.capture_image()
        if frame is None:
            messagebox.showerror("Error", "Failed to capture image")
            return
            
        # Detect and encode face
        face_locations = face_recognition.face_locations(frame)
        if not face_locations:
            messagebox.showerror("Error", "No face detected")
            return
            
        face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
        
        # Save face encoding and image
        self.known_face_encodings.append(face_encoding)
        self.known_face_names.append(user_id)
        
        # Save image
        faces_dir = "known_faces"
        if not os.path.exists(faces_dir):
            os.makedirs(faces_dir)
        
        image_path = os.path.join(faces_dir, f"{user_id}.jpg")
        Image.fromarray(frame).save(image_path)
        
        messagebox.showinfo("Success", f"User registered successfully!\nUser ID: {user_id}")
    
    def login(self):
        # Capture image
        frame = self.capture_image()
        if frame is None:
            messagebox.showerror("Error", "Failed to capture image")
            return
            
        # Detect and encode face
        face_locations = face_recognition.face_locations(frame)
        if not face_locations:
            messagebox.showerror("Error", "No face detected")
            return
            
        face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
        
        # Compare with known faces
        matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
        if True in matches:
            first_match_index = matches.index(True)
            name = self.known_face_names[first_match_index]
            messagebox.showinfo("Success", f"Login successful!\nWelcome, {name}")
        else:
            messagebox.showerror("Error", "Face not recognized")
    
    def run(self):
        self.window.mainloop()
        
    def __del__(self):
        if self.cap is not None:
            self.cap.release()

if __name__ == "__main__":
    app = FaceLoginSystem()
    app.run() 