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

def update_options(selected_date,id=None):
    global day_of_week
    day_of_week = selected_date.strftime('%A')
    print(day_of_week)
    sql = "SELECT time FROM time_tabel WHERE admin_id=%s AND day=%s"
    val = ("101", day_of_week)
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

def conf():
    update="UPDATE time_tabel SET admin_id=%s WHERE time=%s and day=%s"
    val=(to.get(),clicked.get(),day_of_week)
    mycursor.execute(update,val)
    mydb.commit()
    messagebox.showinfo("Successful","Schedule change is done",parent=sub)

def compare_and_update_tables():
    query = """
    SELECT t.time, t.day, t.admin_id AS admin_id_time_table, r.admin_id AS admin_id_rollbk
    FROM time_tabel t
    INNER JOIN rollbk r ON t.time = r.time AND t.day = r.day
    WHERE t.admin_id <> r.admin_id;
    """
    mycursor.execute(query)
    discrepancies = mycursor.fetchall()

    if discrepancies:
        updates_made = 0
        for discrepancy in discrepancies:
            # Access elements by index
            admin_id_rollbk = discrepancy[3]
            time = discrepancy[0]
            day = discrepancy[1]

            # Update time_tabel to use admin_id from rollbk
            update_query = """
            UPDATE time_tabel
            SET admin_id = %s
            WHERE time = %s AND day = %s;
            """
            mycursor.execute(update_query, (admin_id_rollbk, time, day))
            updates_made += mycursor.rowcount

        mydb.commit()
        messagebox.showinfo("Comparison Result", f"Updated {updates_made} discrepancies.", parent=sub)
    else:
        messagebox.showinfo("Comparison Result", "No discrepancies found.", parent=sub)

    mycursor.close()


mydb = mysql.connector.connect(host="localhost", user="root", password="", database="facee")
mycursor = mydb.cursor()

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
co.place(relx=0.5, rely=0.7, relheight=0.1, relwidth=0.35)

re = tk.Button(sub, text="Reset time table", bg='#0a94b0', command=compare_and_update_tables)
re.place(relx=0.13, rely=0.7, relheight=0.1, relwidth=0.35)

sub.mainloop()