import cv2
import os
import numpy as np
import threading
import dlib
import mysql.connector
from src.anti_spoof_predict import AntiSpoofPredict
from src.generate_patches import CropImage
from src.utility import parse_model_name
import face_recognition

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="facee")
mycursor = mydb.cursor()
mycursor.execute("SELECT login_id, face_image FROM face_id_data3")
data = mycursor.fetchall()

# Load pre-built classifier for Frontal Face detection
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# Thread-safe variables
frame_lock = threading.Lock()

# Font style
font = cv2.FONT_HERSHEY_SIMPLEX

skip_frames = 3
frame_count = 0

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
        return False, None  # Return False and None when no encoding found
    database_face_encoding = database_face_encodings[0]

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces in the frame
    face_locations = face_recognition.face_locations(frame_rgb)
    if not face_locations:
        return False, None  # Return False and None when no face detected

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
            return True, matched_face  # Return True and the matched face image

    return False, None  # Return False and None if no match found


def makess(model_test, image, model_dir):
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
    return label == 1

def check_image(image):
    if image is None:
        print("Error: Image is None.")
        return False
    height, width, channel = image.shape if len(image.shape) == 3 else (0, 0, 0)
    if height == 0 or width == 0:
        print("Error: Unable to get image dimensions.")
        return False
    return True

# Open webcam
cap = cv2.VideoCapture(0)

if __name__ == "__main__":
    model_test = AntiSpoofPredict(device_id=0)
    image_cropper = CropImage()

    while True:
        ret, frame = cap.read()

        sql = "UPDATE face_id_data3 SET Present='1' WHERE login_id = %s"

        if not ret:
            print("Failed to capture frame. Exiting...")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        
        # Perform real-time detection
        with frame_lock:
            # For each face in faces, compare with faces in the database
            for (x, y, w, h) in faces:
                # Crop the face region from the frame
                face_region = gray[y:y+h, x:x+w]
                face_region_color = frame[y:y+h, x:x+w]
                for (face_id, face_data) in data:
                    if makess(model_test, face_region_color, model_dir="./resources/anti_spoof_models"):#if one face is real and another is image i will identify both as real
                            match, fac = recognize_face(face_region, face_data)
                            print("Face ID:", face_id)
                            if match:
                                a=str(face_id)
                                va=(a,)
                                mycursor.execute(sql,va)
                                mydb.commit()
                                print(va)
                                # Draw a rectangle around the face and put text describing who is in the picture
                                cv2.rectangle(frame, (x-20, y-20), (x+w+20, y+h+20), (0, 255, 0), 4)
                                cv2.rectangle(frame, (x-22, y-90), (x+w+22, y-22), (0, 255, 0), -1)
                                cv2.putText(frame, f"Name: {face_id} ", (x, y-40), font, 1, (255, 255, 255), 3)
                                break  # Break the loop once a match is found
            # Display the resulting frame
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break