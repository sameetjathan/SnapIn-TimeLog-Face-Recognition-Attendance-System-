from datetime import datetime
from tkinter import ttk
import cv2
import numpy as np
import os
import mysql.connector
import face_recognition
import tkinter as tk
from PIL import Image, ImageTk
from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.utility import parse_model_name

# Assuming the face recognition and AntiSpoofPredict classes are correctly implemented and imported
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# Font style
font = cv2.FONT_HERSHEY_SIMPLEX
class FaceRecognitionApp:
    def __init__(self, parent=None):
        self.parent=parent
        self.window = tk.Toplevel(parent)
        
        self.mydb = mysql.connector.connect(host="localhost", user="root", password="", database="facee")
        self.mycursor = self.mydb.cursor()

        self.window.title("Face Recognition App")

        self.window.attributes('-fullscreen', True)

        self.bg_image_original = Image.open("bg4.jpg")
        self.bg_image_resized = self.bg_image_original.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image_resized)

        # Display the background image using a label
        self.bg_label = tk.Label(self.window, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.bind('<Configure>', self.resize_image)
        self.bg_label.image = self.bg_photo
        self.photo = None

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(self.window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.place(relx=0.26,rely=0.1)
        
        self.btn_quit = tk.Button(self.window, text="Quit",bg='#0a94b0', command=None)
        self.btn_quit.place(relx=0.01, rely=0.03, relwidth=0.1,relheight=0.07)
        self.recognized_faces=[]

        self.update()

    def resize_image(self, event):
        new_width = event.width
        new_height = event.height
        self.bg_image_resized = self.bg_image_original.resize((new_width, new_height))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image_resized)
        self.bg_label.config(image=self.bg_photo)
        self.bg_label.image = self.bg_photo

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            self.process_frame(frame)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            face_region = frame[y:y+h, x:x+w]
            match_found, face_data, face_coords = self.recognize_face(face_region)
            if match_found:
                self.handle_database_update(face_data, face_coords)
    
    #def check_image(image):
    #    if image is None:
    #        print("Error: Image is None.")
    #        return False
    #    height, width, channel = image.shape if len(image.shape) == 3 else (0, 0, 0)
    #    if height == 0 or width == 0:
    #        print("Error: Unable to get image dimensions.")
    #        return False
    #    return True

    def makess(self,model_test, image, model_dir, image_cropper):
        #result = check_image(image)
        #if result is False:
        #    return False
        image_bbox = model_test.get_bbox(image)
        prediction = np.zeros((1, 3))
        # Sum the prediction from single model's result
        for model_name in os.listdir(model_dir):
            h_input, w_input, model_type, scale = parse_model_name(model_name)
            param = {
                "org_img": image,
                "bbox": image_bbox,
                "scale": scale,
                "out_w": w_input,
                "out_h": h_input,
                "crop": True,
            }
            if scale is None:
                param["crop"] = False
            img = image_cropper.crop(**param)
            prediction += model_test.predict(img, os.path.join(model_dir, model_name))
    
        # Draw result of prediction
        label = np.argmax(prediction)
        value = prediction[0][label] / 2
        print("Prediction value: {:.2f}".format(value))
        return label == 1
    
    def fetch_known_faces(self):
        """ Fetch known face encodings and their corresponding IDs from the database. """
        sql="SELECT login_id, face_image FROM face_id_data3 where Department=%s and sem=%s"
        val=('CSE','4')
        self.mycursor.execute(sql,val)
        rows = self.mycursor.fetchall()
        
        known_face_ids = []
        known_face_encodings = []
        
        for row in rows:
            face_id, face_encoding_blob = row
            # Assume face_encoding_blob is stored in a binary format that needs to be converted back to a numpy array
            face_encoding = np.frombuffer(face_encoding_blob, dtype=np.float64)  # Adjust dtype according to how you store the array
            
            known_face_ids.append(face_id)
            known_face_encodings.append(face_encoding)

        return known_face_encodings, known_face_ids

    def recognize_face(self, face_region):
        face_region_rgb = cv2.cvtColor(face_region, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(face_region_rgb)
        face_encodings = face_recognition.face_encodings(face_region_rgb, face_locations)

        if face_encodings:
            face_encoding = face_encodings[0]
            known_face_encodings, known_face_ids = self.fetch_known_faces()
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index] and face_distances[best_match_index] < 0.4:  # using a stricter threshold of 0.4
                return True, known_face_ids[best_match_index], face_locations[0]

        return False, None, None


    def handle_database_update(self, face_data, face_coords):
        # Update database logic
        # Example:
        # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # va = (current_time, face_id)
        # mycursor.execute(sql, va)
        # mydb.commit()
        pass

app = FaceRecognitionApp()
app.window.mainloop()
