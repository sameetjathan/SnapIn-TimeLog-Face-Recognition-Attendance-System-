import customtkinter as ctk
class SlidePanel(ctk.CTkFrame):
	def __init__(self, parent, start_pos, end_pos):
		super().__init__(master = parent)

		# general attributes 
		self.start_pos = start_pos + 0.04
		self.end_pos = end_pos - 0.02
		self.width = abs(start_pos - end_pos)

		
		# animation logic
		self.pos = self.end_pos
		self.in_start_pos = True

		# layout
		self.place(relx = self.end_pos,  rely = 0.14, relwidth = self.width, relheight = 0.7)

	def animate(self):
		if self.in_start_pos:
			self.animate_backwards()
		else:
			self.animate_forward()

	def animate_forward(self):
		if self.pos > self.end_pos:
			self.pos -= 0.009
			self.place(relx = self.pos, rely = 0.14, relwidth = self.width, relheight = 0.7)
			self.after(10, self.animate_forward)
		else:
			self.in_start_pos = True

	def animate_backwards(self):
		if self.pos < self.start_pos:
			self.pos += 0.009
			self.place(relx = self.pos, rely = 0.14, relwidth = self.width, relheight = 0.7)
			self.after(10, self.animate_backwards)
		else:
			self.in_start_pos = False