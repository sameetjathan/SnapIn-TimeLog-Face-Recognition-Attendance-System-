def handle_cell_click(self, event):
    def che():
        self.time_list.remove((start_hour, start_minute, duration))
        self.new = tk.Toplevel(self.loged)
        self.opne = FaceRecognitionApp(self.new, callback=lambda: self.on_face_recognition_close(lec_info, id, bra, sem))
        print("Opening Face Recognition App...")

    def no():
        ta.destroy()

    def open_face_recognition():
        self.loged.withdraw()
        self.loged.after(2000, che)  # Wait for 2 seconds before opening FaceRecognitionApp

    region = event.widget.identify_region(event.x, event.y)
    if region == "cell":
        item = self.tree.identify_row(event.y)
        self.values = self.tree.item(item, 'values')
        id = self.values[0]
        clicked_time = self.values[1]
        lec_info = self.values[3]
        bra = self.values[4]
        sem = self.values[5]
        # Convert the clicked_time string to a tuple of integers
        clicked_hour, clicked_minute, _ = map(int, clicked_time.split(":"))
        clicked_time_tuple = (clicked_hour, clicked_minute)
        found = False
        for start_hour, start_minute, duration in self.time_list:
            if (start_hour, start_minute) == clicked_time_tuple:
                start_time = datetime.datetime.combine(datetime.date.today(), datetime.time(start_hour, start_minute))
                end_time = start_time + datetime.timedelta(hours=int(duration))
                if start_time.time() <= self.current_time <= end_time.time():
                    ta = tk.Toplevel(self.loged)
                    law = tk.Label(ta, text="Do you want to mark attendance?")
                    law.pack()
                    ba = tk.Button(ta, text="Yes", command=open_face_recognition)
                    ba.pack()
                    ba1 = tk.Button(ta, text="No", command=no)
                    ba1.pack()
                    found = True
                    break
        if not found:
            messagebox.showerror("Lecture", "Not time for this lecture")
