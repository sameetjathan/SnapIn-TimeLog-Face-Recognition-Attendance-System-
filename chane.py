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

def update_options(selected_date):
    day_of_week = selected_date.strftime('%A')
    today = datetime.date.today()
    sql = """
    SELECT COALESCE(tc.time, t.time) AS time
    FROM time_tabel t
    LEFT JOIN TemporaryChanges tc ON t.time = tc.time AND t.day = tc.day AND tc.expiration_date > %s
    WHERE t.admin_id = %s AND t.day = %s
    """
    val = (today, '101', day_of_week)  # assuming admin_id '101' is an example
    mycursor.execute(sql, val)
    new_options = [item[0] for item in mycursor.fetchall()]
    menu = drop['menu']
    menu.delete(0, 'end')
    for option in new_options:
        menu.add_command(label=option, command=lambda value=option: clicked.set(value))
    if new_options:
        clicked.set(new_options[0])
    else:
        clicked.set('No times available')

def restore_timetable():
    today = datetime.date.today()
    mycursor.execute("DELETE FROM TemporaryChanges WHERE expiration_date <= %s", (today,))
    mydb.commit()


def popup_calendar():
    top = Toplevel(sub)
    cal = Calendar(top, selectmode='day')
    cal.pack(pady=20, padx=20)

    def on_date_select():
        selected_date = cal.selection_get()
        day_of_week = selected_date.strftime('%A')
        formatted_date = selected_date.strftime('%Y-%m-%d')
        date_entry.delete(0, tk.END)
        date_entry.insert(0,formatted_date)
        update_options(selected_date)
        top.destroy()

    ok_btn = tk.Button(top, text="OK", command=on_date_select)
    ok_btn.pack(pady=10)

def conf():
    try:
        selected_date1 = datetime.datetime.strptime(date_entry.get(), "%Y-%m-%d")
        expiration_date = selected_date1 + datetime.timedelta(days=1)  # Set expiration date to the next day
        day_of_week = selected_date1.strftime('%A')
        insert_query = """
        INSERT INTO TemporaryChanges (admin_id, time, day, expiration_date)
        VALUES (%s, %s, %s, %s);
        """
        val = (to.get(), clicked.get(), day_of_week, expiration_date.date())
        mycursor.execute(insert_query, val)
        mydb.commit()
        messagebox.showinfo("Successful", "Temporary schedule change is done", parent=sub)
        sub.destroy()
    except Exception as e:
        messagebox.showerror("Error", "Invalid date or data entry.", parent=sub)

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="facee")
mycursor = mydb.cursor()
mycursor.execute("""CREATE TABLE IF NOT EXISTS TemporaryChanges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    admin_id VARCHAR(255),
    time VARCHAR(255), -- Keeping as VARCHAR if that's what's used in time_tabel
    duration VARCHAR(255),
    day VARCHAR(255),
    subject VARCHAR(255),
    branch VARCHAR(255),
    sem VARCHAR(233),
    expiration_date DATE,
    FOREIGN KEY (admin_id) REFERENCES time_tabel(admin_id)  -- Adjust the foreign key reference if needed
);
""")

sub = tk.Tk()
sub.geometry('550x400')
bg_image_original = Image.open("bg4change.jpg")
bg_image_resized = bg_image_original.resize((550, 400))
bg_photo = ImageTk.PhotoImage(bg_image_resized)

bg_label = tk.Label(sub, image=bg_photo)
bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
bg_label.bind('<Configure>', resize_image)
bg_label.image = bg_photo

to=tk.Entry(sub,font=('Helvetica bold', 12))
to.place(relx=0.305,rely=0.3,relwidth=0.5,relheight=0.083)

date_entry = tk.Entry(sub, font=('Helvetica bold', 12))
date_entry.place(relx=0.305, rely=0.42, relwidth=0.5, relheight=0.07)
date_entry.bind("<Button-1>", lambda event: popup_calendar())

clicked = tk.StringVar(sub)
clicked.set("Choose a time")

drop = ttk.OptionMenu(sub, clicked, "Choose a time", ())
drop.place(relx=0.306, rely=0.526, relheight=0.078, relwidth=0.4)

co = tk.Button(sub, text="Confirm", bg='#0a94b0', command=conf)
co.place(relx=0.28, rely=0.7, relheight=0.1, relwidth=0.45)

sub.mainloop()
