from tkinter import ttk
import customtkinter as ctk
import numpy as np
import util1
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import face_recognition
import cv2
import os
import mysql.connector
from PIL import Image, ImageTk
from test import *
class register:
    def __init__(self,parent,bg_photo):
        self.parent = parent
        self.mydb = mysql.connector.connect(host="localhost", user="root", password="", database="facee")
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS face_id_data2 (
            login_id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255),
            Gender VARCHAR(255),
            Department VARCHAR(255),
            sem VARCHAR(255),
            face_image BLOB
        );""")
        
        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS face_id_data3 (
            login_id VARCHAR(255) PRIMARY KEY,
            face_image BLOB,
            Present VARCHAR(255),
            Department VARCHAR(255),
            sem VARCHAR(255),
            Arrived VARCHAR(255)
        );""")
        self.bg_photo=bg_photo
        self.root = parent
        self.root.title("Face recognition")
        self.root.configure(bg='#A8DEEA')
        self.root.attributes('-fullscreen', True)
        
        image_path = os.path.abspath("bg44.png")
        self.bg_image_original = Image.open(image_path)
        self.bg_image_resized = self.bg_image_original.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image_resized)

        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.bind('<Configure>', self.resize_image)

        #cag=self.resize_imageb('cap.png', relwidth=0.5, relheight=0.33)
        self.capture1 = tk.Button(self.root,command=self.capturee,compound='center',text="Capture",bg='#0d6e81',activebackground="black",activeforeground="white",font=('Helvetica bold', 12))
        self.capture1.place(relx=0.63, rely=0.78,relwidth=0.2,relheight=0.07)

        self.namee=util1.get_entry_text(self.root)
        self.namee.place(relx=0.69,rely=0.257)

        self.ide=util1.get_entry_text(self.root)
        self.ide.place(relx=0.69,rely=0.36)
        self.v = StringVar(self.root, "0")
        values = {"Male" : "1","Female" : "2",}
        m=tk.Radiobutton(self.root,text="Male",variable=self.v,value=values["Male"],font=("sans-serif", 15),bg='#01589e')
        m.place(relx=0.69,rely=0.455)
        f=tk.Radiobutton(self.root,text="Female",variable=self.v,value=values["Female"],font=("sans-serif", 15),bg='#01589e')
        f.place(relx=0.78,rely=0.455)
        options = ["",
            "CSE",
            "CE",
            "EXTC",
            "IT",]
        self.clicked = StringVar()
        self.clicked.set("CSE")
        style = ttk.Style()
        style.configure("TMenubutton", background="#01589e")
        style.configure("TCombobox", background="#01589e", foreground='red')
        drop = ttk.OptionMenu(self.root, self.clicked, *options)
        drop.place(relx=0.69,rely=0.576)
        drop.config(width=30)
        self.sem = util1.get_entry_text(self.root)
        self.sem.place(relx=0.69,rely=0.676)
        self.btm=util1.get_buttonb(self.root, 'Back to main', 'gray',self.back_to_main, fg='black')
        self.btm.place(relx=0.9,rely=0.01,relwidth=0.09)
        self.webcaml = util1.get_img_label(self.root)
        self.webcaml.place(relx=0.040,rely=0.15)
        self.add_webcam(self.webcaml)
        self.root.bind('<Escape>',self.clse)
        self.root.mainloop()
    
    def back_to_main(self):
        self.root.destroy()
        self.parent.create_main_window()
    
    def clse(self,event):
        self.root.destroy()

    def resize_image(self, event):
        new_width = event.width
        new_height = event.height
        try:
            self.bg_image_resized = self.bg_image_original.resize((new_width, new_height))
            self.bg_photo = ImageTk.PhotoImage(self.bg_image_resized)
            self.bg_label.config(image=self.bg_photo)
        except Exception as e:
            print("Error resizing image:", e)


    def resize_imageb(self,image_path, relwidth, relheight):
        # Open the image file using PIL and preserve the original color space and gamma information
        original_image = Image.open(image_path).convert('RGB')
        
        # Calculate the new dimensions based on relative width and height
        new_width = int(original_image.width * relwidth)
        new_height = int(original_image.height * relheight)
        
        # Resize the image
        resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        
        # Convert the resized image to a PhotoImage object using ImageTk.PhotoImage
        return ImageTk.PhotoImage(resized_image)

    def check_image(self,frame, face_data):
        # Convert the face image from bytes to numpy array
        face_array = np.frombuffer(face_data, dtype=np.uint8)
        database_face = cv2.imdecode(face_array, cv2.IMREAD_COLOR)
    
        # Convert the database face to RGB (as face_recognition library expects RGB)
        database_face_rgb = cv2.cvtColor(database_face, cv2.COLOR_BGR2RGB)
    
        # Encode the face
        database_face_encodings = face_recognition.face_encodings(database_face_rgb)
        if not database_face_encodings:
            return False
        database_face_encoding = database_face_encodings[0]
    
        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        # Detect faces in the frame
        face_locations = face_recognition.face_locations(frame_rgb)
        if not face_locations:
            return False
    
        # Encode the faces found in the frame
        frame_face_encodings = face_recognition.face_encodings(frame_rgb, face_locations)
    
        # Compare the face encodings
        for frame_face_encoding in frame_face_encodings:
            # Calculate the Euclidean distance between the face encodings
            distance = np.linalg.norm(frame_face_encoding - database_face_encoding)
            # Set a threshold for face matching
            threshold = 0.5  # Adjust this value based on your requirement
            
            if distance < threshold:
                return True
        return False


    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        self._label = label
        self.process_webcam()

    def process_webcam(self):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(1, cv2.CAP_MSMF)
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)
        

    def capturee(self):
        self.caturew = tk.Toplevel(self.root)
        self.caturew.geometry("1800x520+50+120")
        bg_image_original = Image.open("bg4.jpg")
        bg_image_resized = bg_image_original.resize((1800,520))
        bg_photo = ImageTk.PhotoImage(bg_image_resized)

        #display the background image using a label
        bg_label = tk.Label(self.caturew, image=bg_photo)
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        bg_label.bind('<Configure>', self.resize_image)

        self.accept_button_register_new_user_window = Button(self.caturew, text='Accept', command=self.accept_register_new_user, bg='green')
        self.accept_button_register_new_user_window.place(x=750, y=300)
        self.try_again_button = Button(self.caturew, text='Try again', command=self.try_again_register_new_user, bg='red')
        self.try_again_button.place(x=750, y=400)

        self.capture_label = Label(self.caturew,bg="#0a94b0")

        self.capture_label.place(x=10, y=0, width=700, height=500)
        self.add_img_to_label(self.capture_label)
        self.caturew.mainloop()

    def try_again_register_new_user(self):
        self.caturew.destroy()

    def accept_register_new_user(self):
        student_name = self.namee.get(1.0, "end-1c")
        login_id = self.ide.get(1.0, "end-1c")
        gender = "Female" if self.v.get() == '2' else "Male"
        department = self.clicked.get()
        sem=self.sem.get(1.0, "end-1c")
        
        # Convert the captured image to bytes
        image_bytes = cv2.imencode('.jpg', self.register_new_user_capture)[1].tobytes()
        
        # Insert the details and face image bytes into the database
        self.mycursor.execute('SELECT * FROM face_id_data2 WHERE login_id=%s', (login_id,))
        data = self.mycursor.fetchone()
        print(data)
        if data is not None:
            messagebox.showerror('Error', 'Login ID already exists.')
            return
        
        # Insert data into face_id_data2 and face_id_data3 tables
        self.mycursor.execute('INSERT INTO face_id_data2 (login_id, name, Gender, Department,sem, face_image) VALUES (%s, %s, %s, %s, %s,%s)', 
                               (login_id, student_name, gender, department,sem, image_bytes))
        self.mycursor.execute('INSERT INTO face_id_data3 (login_id, face_image, Present,sem,Arrived,Department) VALUES (%s, %s, %s,%s,%s,%s)', 
                               (login_id, image_bytes, '0',sem,"None",department))
        
        # Commit changes to the database
        self.mydb.commit()
        
        # Show success message
        messagebox.showinfo('Success', 'Face ID registered successfully.')
        
        # Clear the entry fields
        self.namee.delete(1.0, tk.END)
        self.ide.delete(1.0, tk.END)
        
        # Close the capture window
        self.caturew.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_arr.copy()
        #check if face already exist or not
        self.mycursor.execute("SELECT login_id, face_image FROM face_id_data3")
        data1 = self.mycursor.fetchall()
        for (face_id, face_data) in data1:
            match = self.check_image(self.register_new_user_capture,face_data)
            if match:
                messagebox.showerror('Error', f'{face_id} already exist',parent=self.root)
                return

if __name__ == "__main__":
    rooe=tk.Tk()
    app = register(parent=rooe,bg_photo=None)  
    rooe.mainloop()