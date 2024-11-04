import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from PIL import Image, ImageTk
from tkcalendar import Calendar
import mysql.connector
import datetime

def resize_image(event):
    new_width = event.width
    new_height = event.height
    bg_image_resized = bg_image_original.resize((new_width, new_height))
    bg_photo = ImageTk.PhotoImage(bg_image_resized)
    bg_label.config(image=bg_photo)
    bg_label.image = bg_photo

def conf():
    update="UPDATE time_tabel SET admin_id=%s WHERE time=%s"
    val=(to.get(),clicked.get())
    mycursor.execute(update,val)
    mydb.commit()
    messagebox.showinfo("Successful","Schedule change is done",parent=sub)

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="facee")
mycursor = mydb.cursor()

sub = tk.Tk()
sub.geometry('300x200')
bg_image_original = Image.open("bgdown.jpg")
bg_image_resized = bg_image_original.resize((300,200))
bg_photo = ImageTk.PhotoImage(bg_image_resized)

bg_label = tk.Label(sub, image=bg_photo)
bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
bg_label.bind('<Configure>', resize_image)
bg_label.image = bg_photo

sql = "SELECT subject FROM facedata4 WHERE admin_id=%s"
val = ('101',)
mycursor.execute(sql, val)
clicked = tk.StringVar(sub)
clicked.set("Choose a subject")  # default value
style = ttk.Style()
options = [item[0] for item in mycursor.fetchall()] 
style.configure("TMenubutton", background="#01589e")
style.configure("TCombobox", background="#01589e", foreground='red')
drop = ttk.OptionMenu(sub, clicked, clicked.get(), *options)
drop.place(relx=0.17,rely=0.2,relheight=0.16,relwidth=0.7)
co=tk.Button(sub,text="confirm",fg='white',font=('Times Roman', 13),bg='#0000ff',command=None)
co.place(relx=0.17,rely=0.6,relheight=0.2,relwidth=0.7)
sub.mainloop()

