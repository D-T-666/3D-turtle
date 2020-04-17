from tkinter import *
from tkinter import font as tkFont

pi = 14159


# I'll be back soon!



class Control_panel:
	def __init__(self):
		self.root = Tk()

		# sliders
		self.s_rx = Scale(self.root, orient=HORIZONTAL, from_=-pi, to=pi, resolution=0.1, length=200)
		self.s_ry = Scale(self.root, orient=HORIZONTAL, from_=-pi, to=pi, resolution=0.1, length=200)
		self.s_rz = Scale(self.root, orient=HORIZONTAL, from_=-pi, to=pi, resolution=0.1, length=200)
		self.s_px = Scale(self.root, orient=HORIZONTAL, from_=-10, to=10, resolution=0.1, length=200)
		self.s_py = Scale(self.root, orient=HORIZONTAL, from_=-10, to=10, resolution=0.1, length=200)
		self.s_pz = Scale(self.root, orient=HORIZONTAL, from_=-10, to=10, resolution=0.1, length=200)
		self.create_text(text='rotation x', col=0, row=0)
		self.create_text(text='rotation y', col=0, row=2)
		self.create_text(text='rotation z', col=0, row=4)
		self.create_text(text='position x', col=0, row=6)
		self.create_text(text='position y', col=0, row=8)
		self.create_text(text='position z', col=0, row=10)
		self.s_rx.grid(column=0, row=1, sticky=W)
		self.s_ry.grid(column=0, row=3, sticky=W)
		self.s_rz.grid(column=0, row=5, sticky=W)
		self.s_px.grid(column=0, row=7, sticky=W)
		self.s_py.grid(column=0, row=9, sticky=W)
		self.s_pz.grid(column=0, row=11, sticky=W)

		# checkboxes
		self.v_stroke = False
		self.v_fill = False
		self.c_stroke = Checkbutton(self.root, text="stroke", command=self.stroke_changed)
		self.c_fill = Checkbutton(self.root, text="fill", command=self.fill_changed)
		self.c_stroke.grid(column=0, row=12, sticky=W)
		self.c_fill.grid(column=0, row=12, sticky=E)

	def create_text(self, text='###', row=0, col=0):
		Label(self.root, text=text).grid(row=row, column=col)

	def stroke_changed(self):
		self.v_stroke = not self.v_stroke

	def fill_changed(self):
		self.v_fill = not self.v_fill

	def get_vars(self):
		return [self.s_px.get(),
				self.s_py.get(),
				self.s_pz.get(),
				self.s_rx.get(),
				self.s_ry.get(),
				self.s_rz.get(),
				self.v_stroke,
				self.v_fill]

	def get_root(self):
		return self.root