from datetime import datetime
import io
import threading
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
import time


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


mydb = mysql.connector.connect(host="localhost", user="root", password="", database="facee")
mycursor = mydb.cursor()


# Create classifier from pre-built model
# Load pre-built classifier for Frontal Face detection
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# Font style
font = cv2.FONT_HERSHEY_SIMPLEX

# Function to recognize faces from database
def recognize_face(frame, face_data):
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

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(frame_rgb)
    if not face_locations:
        return False, None, None  # Return False, None, and None when no face detected

    # Encode the faces found in the frame
    frame_face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)

    # Compare the face encodings
    for (top, right, bottom, left), frame_face_encoding in zip(face_locations, frame_face_encodings):
        # Calculate the Euclidean distance between the face encodings
        distance = np.linalg.norm(frame_face_encoding - database_face_encoding)
        print("Distance between face encodings:", distance)

        # Set a threshold for face matching
        threshold = 0.5  # Adjust this value based on your requirement
        if distance < threshold:
            matched_face = frame[top:bottom, left:right]
            return True, matched_face, (top, right, bottom, left)  # Return True, the matched face image, and face coordinates

    return False, None, None  # Return False, None, and None if no match found


#def recognize_face(frame, face_data):
#    # Convert the face image from bytes to numpy array
#    face_array = np.frombuffer(face_data, dtype=np.uint8)
#    database_face = cv2.imdecode(face_array, cv2.IMREAD_COLOR)
#
#    # Convert the database face to RGB (as face_recognition library expects RGB)
#    database_face_rgb = cv2.cvtColor(database_face, cv2.COLOR_BGR2RGB)
#
#    # Encode the face
#    database_face_encodings = face_recognition.face_encodings(database_face_rgb)
#    if not database_face_encodings:
#        print("Error: No face encoding found for the database face.")
#        return False, None
#    database_face_encoding = database_face_encodings[0]
#
#    # Convert the frame to RGB
#    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#    # Detect faces in the frame
#    face_locations = face_recognition.face_locations(frame_rgb)
#    if not face_locations:
#        return False, None
#
#    # Encode the faces found in the frame
#    frame_face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)
#
#    # Compare the face encodings
#    for frame_face_encoding, (top, right, bottom, left) in zip(frame_face_encodings, face_locations):
#        # Calculate the Euclidean distance between the face encodings
#        distance = np.linalg.norm(frame_face_encoding - database_face_encoding)
#        print("Distance between face encodings:", distance)
#
#        # Set a threshold for face matching
#        threshold = 0.5  # Adjust this value based on your requirement
#        
#        if distance < threshold:
#            return True, (top, right, bottom, left)
#
#    return False, None

def makess(model_test, image, model_dir, image_cropper):
    result = check_image(image)
    if result is False:
        return False
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
    return label==1

def check_image(image):
    if image is None:
        print("Error: Image is None.")
        return False
    height, width, channel = image.shape if len(image.shape) == 3 else (0, 0, 0)
    if height == 0 or width == 0:
        print("Error: Unable to get image dimensions.")
        return False
    return True

class FaceRecognitionApp:
    def __init__(self,parent=None,callback=None,bra=None,sem=None):
        self.parent=parent
        self.callback = callback 
        
        sql="SELECT login_id, face_image FROM face_id_data3 where Department=%s and sem=%s"
        val=(bra,sem)
        mycursor.execute(sql,val)
        self.data = mycursor.fetchall()
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

#        sql="SELECT login_id,Present,Arrived from face_id_data3"
#        self.mycursor.execute(sql)
#        self.res = self.mycursor.fetchall()
        self.frame_lock=threading.Lock() 
        self.video_source = 2
        self.vid = cv2.VideoCapture(self.video_source)
#
#        frame = tk.Frame(self.window)
#        frame.place(relx=0.1, rely=0.67, relwidth=0.8, relheight=0.2999)
#
#        self.tree = ttk.Treeview(frame, columns=(1, 2, 3), show="headings", height=len(self.res))
#        self.tree.grid(row=0, column=0, sticky="nsew")  # Use grid() instead of pack()
#
#        self.tree.heading(1, text="Login ID")
#        self.tree.heading(2, text="Present")
#        self.tree.heading(3, text="Arrived time")
#
#        for row in self.res:
#            self.tree.insert('', 'end', values=row)
#        
#        self.tree.bind('<Button-1>', self.handle_click)
#        #self.tree.bind("<ButtonRelease-1>", self.handle_cell_click)
#        
#        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
#        scrollbar.grid(row=0, column=1, sticky="ns")
#        self.tree.configure(yscrollcommand=scrollbar.set)
#        
#        scrollbar1 = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
#        scrollbar1.grid(row=1, column=0, sticky="ew") 
#        self.tree.configure(xscrollcommand=scrollbar1.set)
#        
#        # Configure row and column weights to allow expansion
#        frame.grid_rowconfigure(0, weight=1)
#        frame.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.place(relx=0.26,rely=0.1)
        
        self.btn_quit = tk.Button(self.window, text="Quit",bg='#0a94b0', command=self.quit)
        self.btn_quit.place(relx=0.01, rely=0.03, relwidth=0.1,relheight=0.07)
        self.recognized_faces=[]
        
        self.update()

#    def handle_click(self,event):
#            if self.tree.identify_region(event.x, event.y) == "separator":
#               return "break"
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
            match_found, face_coords = self.find_match(frame)
            if match_found:
                top, right, bottom, left = face_coords
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 4)
                cv2.putText(frame, f"ID: {self.matched_face_id} ", (left, top-20), font, 1, (255, 255, 255), 3)
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)         
            self.window.after(10, self.update)

    def find_match(self, frame):
            sql = "UPDATE face_id_data3 SET Present='1', Arrived=%s WHERE login_id = %s"
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            
            with self.frame_lock:
                for (x, y, w, h) in faces:
                    face_region_color = frame[y:y+h, x:x+w]
                    
                    # Filter faces based on proximity (example: centroid distance)
                    filtered_faces = self.filter_faces_by_proximity(x, y, w, h)
                    print("goo")
                    for (face_id, face_data) in filtered_faces:
                        print("in")
                        if face_id not in self.recognized_faces:
                            match, fac, face_coords = recognize_face(frame, face_data)
                            if match:
                                if makess(model_test=AntiSpoofPredict(device_id=0), image=face_region_color, model_dir="./resources/anti_spoof_models", image_cropper=CropImage()):
                                    self.matched_face_id = face_id
                                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    va = (current_time, face_id)
                                    self.mycursor.execute(sql, va)
                                    self.mydb.commit()
                                    self.recognized_faces.append(face_id)
                                    print("present")
                                    return True, face_coords
                return False, None

    def calculate_centroid(self, image):
            # Calculate moments of the image
            moments = cv2.moments(image[:,:,0])
    
            # Calculate centroid
            if moments["m00"] != 0:
                centroid_x = int(moments["m10"] / moments["m00"])
                centroid_y = int(moments["m01"] / moments["m00"])
                centroid = np.array([centroid_x, centroid_y])
            else:
                centroid = np.array([0, 0])  # Default centroid
    
            return centroid

    def filter_faces_by_proximity(self, x, y, w, h):
        filtered_faces = []

        for (face_id, face_data) in self.data:
            # Example: Assume face_data is stored as BLOB in database
            # Decode BLOB data into an image format
            decoded_image = self.decode_blob_image(face_data)

            # Calculate centroid of the detected face
            detected_face_centroid = np.array([(x + w // 2), (y + h // 2)])
            # Calculate centroid of the face data from database
            db_face_centroid = self.calculate_centroid(decoded_image)

            # Calculate Euclidean distance between centroids
            distance = np.linalg.norm(detected_face_centroid - db_face_centroid)

            # Define a threshold for proximity (adjust as needed)
            proximity_threshold = 50  # Adjust based on your application

            if distance < proximity_threshold:
                filtered_faces.append((face_id, decoded_image))

        return filtered_faces

    def decode_blob_image(self, blob_data):
        # Example function to decode BLOB data into an image format
        image = Image.open(io.BytesIO(blob_data))
        return np.array(image)    
    
    def quit(self):
        if self.vid.isOpened():
            self.vid.release()
        self.window.destroy()
        if self.callback:  # Call the callback method if provided
            self.callback()
            
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root,bra='CSE',sem='4')
    root.mainloop()