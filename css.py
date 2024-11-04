import tkinter as tk
from tkinter import messagebox

def get_label(window, text):
    label = tk.Label(window, text=text,bg="#014172")
    label.config(font=("sans-serif", 21), justify="left")
    return label

def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=0,bg="black",
                       width=20, font=("Arial", 18))
    return inputtxt
def get_buttonb(window, text,bg, command=None , fg='white'):
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="black",
                        activeforeground="white",
                        fg=fg,
                        bg=bg,
                        command=command,
                        height=2,
                        width=10,
                        font=('Helvetica bold', 12)
                    )
    return button
def get_button(window, text, color,image,command, fg='white'):
    button = tk.Button(
                        window,image=image,compound='center',
                        text=text,
                        activebackground="black",
                        activeforeground="white",
                        fg=fg,
                        bg=color,
                        command=command,
                        height=1,
                        width=20,
                        font=('Helvetica bold', 12)
                    )

    return button