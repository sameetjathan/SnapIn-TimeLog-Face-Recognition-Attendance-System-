import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from register import register
from adminlog import adminlog
class Page1:
    def __init__(self):
        self.create_main_window()
        self.help_root = None
        self.newreg = None

    def show_about(self,event):
        about_window = tk.Toplevel(self.root)
        about_window.title("About")
        about_window.geometry("900x600+4+6")
        # Load the original background image
        bg_image_original = Image.open("bg43.jpg")
        bg_image_resized = bg_image_original.resize((900,600))
        bg_photo = ImageTk.PhotoImage(bg_image_resized)

        #display the background image using a label
        bg_label = tk.Label(about_window, image=bg_photo)
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        bg_label.bind('<Configure>', self.resize_image)

        about_window.mainloop()

    def help_info(self,event):
        about_window = tk.Toplevel(self.root)
        about_window.title("Help")
        about_window.geometry("900x630+4+6")
        # Load the original background image
        bg_image_original = Image.open("bg431.jpg")
        bg_image_resized = bg_image_original.resize((900,630))
        bg_photo = ImageTk.PhotoImage(bg_image_resized)

        #display the background image using a label
        bg_label = tk.Label(about_window, image=bg_photo)
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        bg_label.bind('<Configure>', self.resize_image)

        about_window.mainloop()
    
    def contact(self,event):
        about_window = tk.Toplevel(self.root)
        about_window.title("Contact")
        about_window.geometry("400x200+4+6")
        bg_image_original = Image.open("bg44.jpg")
        bg_image_resized = bg_image_original.resize((400,200))
        bg_photo = ImageTk.PhotoImage(bg_image_resized)

        #display the background image using a label
        bg_label = tk.Label(about_window, image=bg_photo)
        bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        bg_label.bind('<Configure>', self.resize_image)
        about_window.mainloop()
        
    def goo(self):
        if self.help_root:
            self.help_root.destroy()
        if self.root:
            self.root.deiconify()

    def start_face_registration_app(self):
        da=tk.Toplevel(self.root)
        daf=register(parent=da,bg_photo=None)
        
    def start_admin_win(self):
        if self.root:
            self.root.destroy()
        self.admin = adminlog(parent=self)
        self.admin.start()

    def resize_image(self, event):
        new_width = event.width
        new_height = event.height
        self.bg_image_resized = self.bg_image_original.resize((new_width, new_height))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image_resized)
        self.bg_label.config(image=self.bg_photo)
        self.bg_label.image = self.bg_photo
    
    def en(self,event):
        if event.widget==self.about_button:
            self.about_button.config(fg='white')
        elif event.widget==self.help_button:
            self.help_button.config(fg='white')
        elif event.widget==self.contact_button:
            self.contact_button.config(fg='white')
    
    def le(self,event):
        if event.widget==self.about_button:
            self.about_button.config(fg='black')
        elif event.widget==self.help_button:
            self.help_button.config(fg='black')
        elif event.widget==self.contact_button:
            self.contact_button.config(fg='black')
    
    # Function to resize image based on relative width and height
    def resize_imageb(self,image_path, relwidth, relheight):
        # Open the image file using PIL and preserve the original color space and gamma information
        original_image = Image.open(image_path).convert('RGB')
        
        # Calculate the new dimensions based on relative width and height
        new_width = int(original_image.width * relwidth)
        new_height = int(original_image.height * relheight)
        
        # Resize the image
        resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        return ImageTk.PhotoImage(resized_image)
    
    def create_linear_gradient(self, width, height, color1, color2):
        image = Image.new("RGB", (width, height), color1)
        draw = ImageDraw.Draw(image)
        for y in range(height):
            r = int(color1[0] * (1 - y / height) + color2[0] * (y / height))
            g = int(color1[1] * (1 - y / height) + color2[1] * (y / height))
            b = int(color1[2] * (1 - y / height) + color2[2] * (y / height))
            # Adjust colors for corners
            if y < height / 2:
                r = max(0, int(r * 0.7))                 
                g = max(0, int(g * 0.7))  
                b = max(0, int(b * 0.7))              
            else:
                r = max(0, int(r * 0.3))
                g = max(0, int(g * 0.3))
                b = max(0, int(b * 0.3))
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        return image

    def clsoe(self,event):
        self.root.destroy()

    def clsoe1(self):
        self.root.destroy()

    def create_main_window(self):
        self.root = tk.Tk()
        self.root.title("Face recognition")
        self.root.configure(bg='#A8DEEA')
        self.root.attributes('-fullscreen', True)
        self.root.state('zoomed')
        
        # Load the original background image
        self.bg_image_original = Image.open("bg4.png")
        self.bg_image_resized = self.bg_image_original.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        #self.bg_image_resized = self.bg_image_original.resize((1350,790))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image_resized)

        # Display the background image using a label
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bg_label.bind('<Configure>', self.resize_image)

        ka=self.resize_imageb('labell.jpg', relwidth=1,relheight=1)
        
        self.about_button = tk.Label(self.root, text="About",compound='center',image=ka, font=("Arial", 16),fg='black')
        self.about_button.place(relx=0.29, rely=0.054,relwidth=0.104,relheight=0.09)
        self.about_button.bind("<Button-1>",self.show_about)
        self.about_button.bind("<Enter>",self.en)
        self.about_button.bind("<Leave>",self.le)

        self.help_button = tk.Label(self.root, text="Help",compound='center',image=ka, font=("Arial", 16))
        self.help_button.place(relx=0.43, rely=0.054,relwidth=0.104,relheight=0.09)
        self.help_button.bind("<Button-1>",self.help_info)
        self.help_button.bind("<Enter>",self.en)
        self.help_button.bind("<Leave>",self.le)
        
        self.contact_button = tk.Label(self.root, text="Contact",compound='center',image=ka, font=("Arial", 16))
        self.contact_button.place(relx=0.57,rely=0.054,relwidth=0.104,relheight=0.09)
        self.contact_button.bind("<Button-1>",self.contact)
        self.contact_button.bind("<Enter>",self.en)
        self.contact_button.bind("<Leave>",self.le)

        relw=35
        relh=20
        
        gradient_photo=self.resize_imageb('button1.jpg', relw, relh)
        register_button = tk.Button(self.root,text="New resgistration",image= gradient_photo,font=("Times Roman", 15), compound='center',command=self.start_face_registration_app, bg='#0d6e81', activebackground='#6DA5C0')
        register_button.config(image=gradient_photo)
        admin_button = tk.Button(self.root, text="Admins Login",image= gradient_photo,font=("sans-serif", 15),compound="center",  bg='#0d6e81', activebackground='#6DA5C0',height=4, width=76,command=self.start_admin_win)

        quit = tk.Button(self.root, text="X", bg='#0d6e81', activebackground='#6DA5C0',command=self.clsoe1,height=2, width=4)
        quit.place(relx=0.9,rely=0.04)
        register_button.place(relx=0.57, rely=0.38, relwidth=0.35,relheight=0.09)
        admin_button.place(relx=0.57, rely=0.58, relwidth=0.35,relheight=0.09)

        self.root.bind("<Escape>",self.clsoe)

        self.root.mainloop()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    Page1()