from tkinter import *
from tkinter import filedialog
import os
import subprocess

w = 300
h = 300
window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry(str(w)+'x' + str(h))
selectedBefore_file = ""
selected_file = ""

turtle_window_pid = 0

def onSelectNewFile():
	# when selected a diffrent file from before from the list box
	# event here
	turtle_window_pid = subprocess.Popen(["python", "./main.py", selected_file]).pid


	pass


def event0(var):
	print("Enable render 0:"+str(var))
	if turtle_window_pid is not None:
	    try:
	        os.kill(turtle_window_pid, 0)
	    except:
	        pass
	pass


def event1(var):
	print("Enable render 1:"+str(var))
	pass


def event2(var):
	print("Enable render 2:"+str(var))
	pass

##############################


def onSelectDifrentFileHandler():
	global selected_file, selectedBefore_file
	if selected_file != selectedBefore_file:
		selectedBefore_file = selected_file
		return True
	return False
# event on select file


def onselectFromListBox(evt):
	global selected_file, selectedBefore_file

	w = evt.widget
	try:
		index = int(w.curselection()[0])
		value = w.get(index)

		selected_file = value
		if onSelectDifrentFileHandler():
			onSelectNewFile()
			pass
	except:
		print("nothing in the list")


def openFile():
	window.filename = filedialog.askopenfilename(
		initialdir="/", title="Select file", filetypes=(("obj files", "*.obj"), ("all files", "*.*")))
	# on import a file
	print(window.filename)
	# add to the list

	en.listSelection.insert(END, str(window.filename))
	return


class Menu:
	def __init__(self, heigh, width):
		self.w = width
		self.h = heigh
		self.buttons = []

		# changeable stuff
		self.vars = [IntVar(), IntVar(), IntVar()]
		# this should be the same as self.vars
		self.Logicvars = [IntVar(), IntVar(), IntVar()]
		# events for each checkbox returns it value
		self.checkboxEvents = [event0, event1, event2]

	def createButton(self, text, width, height, event):

		newthing = Button(window, text=text, width=width,
						  height=height, command=event)

		self.buttons.append(newthing)
		pass

	def varevent(self):
		for i in range(len(self.vars)):
			if self.vars[i].get() != self.Logicvars[i].get():
				self.checkboxEvents[i](self.vars[i].get())
				self.Logicvars[i].set(self.vars[i].get())
		pass

	def showcheckButtons(self):
		Checkbutton(
			window, text="render1",
			variable=self.vars[0], command=self.varevent).grid(column=0, row=len(self.buttons))
		Checkbutton(
			window, text="render2",
			variable=self.vars[1], command=self.varevent).grid(column=0, row=len(self.buttons)+1)
		Checkbutton(
			window, text="render3",
			variable=self.vars[2], command=self.varevent).grid(column=0, row=len(self.buttons)+2)

	def showListView(self):
		self.listSelection = Listbox(
			window, height=15, width=33)
		self.listSelection.grid(row=1, rowspan=5, column=1, padx=5, pady=5)

		# if you want to add in the listBox values by default
		# for x in "ABCDEF":
		#   self.listSelection.insert(END, x )

		self.listSelection.bind('<<ListboxSelect>>', onselectFromListBox)

	def render(self):
		i = 0
		r = 0
		self.showListView()
		while i < len(self.buttons):
			self.buttons[i].grid(column=0, row=i)
			i += 1

		self.showcheckButtons()

		window.mainloop()


en = Menu(300, 500)
en.createButton('openfile', 11, 1, openFile)

en.render()
###############################
