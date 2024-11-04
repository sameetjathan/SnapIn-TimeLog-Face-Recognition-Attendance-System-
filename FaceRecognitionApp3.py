from datetime import datetime
import threading
import queue
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

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="facee")
mycursor = mydb.cursor()

cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
font = cv2.FONT_HERSHEY_SIMPLEX

def recognize_face(face_region, face_data):
    # Convert the face image from bytes to numpy array
    face_array = np.frombuffer(face_data, dtype=np.uint8)
    database_face = cv2.imdecode(face_array, cv2.IMREAD_COLOR)

    # Convert the database face to RGB (as face_recognition library expects RGB)
    database_face_rgb = cv2.cvtColor(database_face, cv2.COLOR_BGR2RGB)

    # Encode the face
    database_face_encodings = face_recognition.face_encodings(database_face_rgb)
    if not database_face_encodings:
        print("Error: No face encoding found for the database face.")
        return False, None, None  # Return False, None, and None when no encoding found
    database_face_encoding = database_face_encodings[0]

    # Convert the face region to RGB
    face_region_rgb = cv2.cvtColor(face_region, cv2.COLOR_BGR2RGB)

    # Encode the face region
    face_region_encodings = face_recognition.face_encodings(face_region_rgb)
    if not face_region_encodings:
        return False, None, None  # Return False, None, and None when no encoding found
    face_region_encoding = face_region_encodings[0]

    # Calculate the Euclidean distance between the face encodings
    distance = np.linalg.norm(face_region_encoding - database_face_encoding)
    print("Distance between face encodings:", distance)

    # Set a threshold for face matching
    threshold = 0.5  # Adjust this value based on your requirement
    if distance < threshold:
        return True, face_region, None  # Return True and the matched face region

    return False, None, None  # Return False, None, and None if no match found


def makess(model_test, image, model_dir, image_cropper):
    if not check_image(image):
        return False
    image_bbox = model_test.get_bbox(image)
    prediction = np.zeros((1, 3))
    for model_name in os.listdir(model_dir):
        h_input, w_input, model_type, scale = parse_model_name(model_name)
        param = {"org_img": image, "bbox": image_bbox, "scale": scale, "out_w": w_input, "out_h": h_input, "crop": True}
        if scale is None:
            param["crop"] = False
        img = image_cropper.crop(**param)
        prediction += model_test.predict(img, os.path.join(model_dir, model_name))
    label = np.argmax(prediction)
    return label == 1

def check_image(image):
    if image is None:
        return False
    height, width, channel = image.shape if len(image.shape) == 3 else (0, 0, 0)
    return height > 0 and width > 0

class FaceRecognitionApp:
    def __init__(self, parent=None, callback=None, bra=None, sem=None):
        self.parent = parent
        self.callback = callback
        sql = "SELECT login_id, face_image FROM face_id_data3 where Department=%s and sem=%s"
        val = (bra, sem)
        mycursor.execute(sql, val)
        self.data = mycursor.fetchall()
        self.window = tk.Toplevel(parent)
        self.mydb = mysql.connector.connect(host="localhost", user="root", password="", database="facee")
        self.mycursor = self.mydb.cursor()
        self.window.title("Face Recognition App")
        self.window.attributes('-fullscreen', True)
        self.bg_image_original = Image.open("bg4.jpg")
        self.bg_image_resized = self.bg_image_original.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image_resized)
        self.bg_label = tk.Label(self.window, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.bind('<Configure>', self.resize_image)
        self.bg_label.image = self.bg_photo
        self.frame_lock = threading.Lock()
        self.video_source = 1
        self.vid = cv2.VideoCapture(self.video_source)
        self.canvas = tk.Canvas(self.window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.place(relx=0.26, rely=0.1)
        self.btn_quit = tk.Button(self.window, text="Quit", bg='#0a94b0', command=self.quit)
        self.btn_quit.place(relx=0.01, rely=0.03, relwidth=0.1, relheight=0.07)
        self.recognized_faces = []
        self.frame_queue = queue.Queue()
        self.stop_flag = threading.Event()
        self.process_thread = threading.Thread(target=self.process_frames)
        self.process_thread.start()
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
        frame=cv2.flip(frame,1)
        if ret:
            self.frame_queue.put(frame)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

    def process_frames(self):
        while not self.stop_flag.is_set():
            try:
                frame = self.frame_queue.get(timeout=1)
                self.find_match(frame)
            except queue.Empty:
                continue

    def find_match(self, frame):
        sql = "UPDATE face_id_data3 SET Present='1', Arrived=%s WHERE login_id = %s"
    
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        # Detect faces in the frame
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        with self.frame_lock:
            # For each face in faces, compare with faces in the database
            for (x, y, w, h) in faces:
                # Crop the face region from the frame
                face_region_color = frame[y:y+h, x:x+w]
                for (face_id, face_data) in self.data:
                    if face_id not in self.recognized_faces:
                        match, fac, face_coords = recognize_face(face_region_color, face_data)
                        print("Face ID:", face_id)  # Print the face ID
                        if match:
                            print('match')
                            if makess(model_test=AntiSpoofPredict(device_id=0), image=fac, model_dir="./resources/anti_spoof_models", image_cropper=CropImage()):
                                self.matched_face_id = face_id
                                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current time
                                va = (current_time, face_id)  # Values for SQL query
                                mycursor.execute(sql, va)  # Execute SQL query
                                mydb.commit()  # Commit changes to database
                                self.recognized_faces.append(face_id)
                                print("present")
                                return True, (y, x+w, y+h, x)
            return False, None

    def quit(self):
        if self.vid.isOpened():
            self.vid.release()
        self.stop_flag.set()  # Signal the thread to stop
        self.frame_queue.put(None)  # Unblock the thread if it's waiting
        self.process_thread.join()  # Wait for the thread to finish
        self.window.destroy()
        if self.callback:
            self.callback()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root, bra="CSE", sem="4")
    root.mainloop()
