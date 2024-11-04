import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import os
import mysql.connector
from PIL import Image, ImageTk, ImageFilter, ImageDraw
from FaceRecognitionApp import FaceRecognitionApp

class loggedin:
    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(host="localhost", user="root", password="", database="facee")
        self.mycursor = self.mydb.cursor()
        self.bg_photo = None
        self.opne=None
        self.logined() 

    def logined(self):
        self.loged = ctk.CTk()
        self.loged.title("Loged")
        self.loged.configure(bg='#A8DEEA')
        self.loged.attributes('-fullscreen', True)

        image_path = os.path.abspath("bg4.jpg")
        self.bg_image_original = Image.open(image_path)
        self.bg_image_resized = self.bg_image_original.resize((self.loged.winfo_screenwidth(), self.loged.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image_resized)
    
        self.bglabel = tk.Label(self.loged, image=self.bg_photo)
        self.bglabel.place(x=0, y=0, relwidth=1, relheight=1)
        self.bglabel.bind('<Configure>', self.resize_image)

        self.backs = tk.Button(self.loged, text="Admin Page", command=self.closw)
        self.backs.pack()
        
        self.lecture1 = tk.Button(self.loged, text="Lecture1", command=self.lec)
        self.lecture1.pack()

        self.lecture2 = tk.Button(self.loged, text="Lecture2", command=self.lec)
        self.lecture2.pack()

        self.mydb.commit()
        self.loged.mainloop()           
    
    def resize_image(self, event):
        new_width = event.width
        new_height = event.height
        self.bg_image_resized = self.bg_image_original.resize((new_width, new_height))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image_resized)
        self.bglabel.config(image=self.bg_photo)
    
    def on_face_recognition_close(self,source_button):
            if source_button == self.lecture1:
                pass
                
            elif source_button == self.lecture2:
                print("Face Recognition App closed from Lecture2 button.")
            else:
                print("Face Recognition App closed from an unknown source.")

    
    def lec(self):
        if self.lecture1:
            self.opne = FaceRecognitionApp(self.loged,  callback=lambda: self.on_face_recognition_close(self.lecture1))
            print("Opening Face Recognition App...")
        elif self.lecture2:
            self.opne = FaceRecognitionApp(self.loged, callback=lambda: self.on_face_recognition_close(self.lecture2))
            print("Opening Face Recognition App from Lecture2 button...")
        
    
    def closw(self):
        self.loged.destroy()

if __name__ == "__main__":
    sa = loggedin()
