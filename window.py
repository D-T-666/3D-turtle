import turtle

class Screen:
	def __init__(self, size_x=600, size_y=600):
		self.screen = turtle.Screen()
		self.screen.setup(size_x, size_y)
		self.screen.colormode(255)
		self.t = turtle.Turtle()
		self.t.speed(0)
		self.t.up()
		self.t.ht();
		self.screen.tracer(0)
	
	def update(self):
		self.t.screen.update()

	def stroke(self, col):
		self.t.pencolor(col)

	def fill(self, col):
		self.t.fillcolor(col)

	def bgcolor(self, col=None):
		if col:
			self.screen.bgcolor(col)
		else:
			return self.screen.bgcolor()

	def drawPolygon(self, face, scl=1, stroke=False, fill=True):
		self.t.goto(face[0][0]*scl, face[0][1]*scl)
		if fill: self.t.begin_fill();
		if stroke: self.t.down();
		for i in range(1,len(face)):
			self.t.goto(face[i][0]*scl, face[i][1]*scl)
		self.t.goto(face[0][0]*scl, face[0][1]*scl)
		if stroke: self.t.up();
		if fill: self.t.end_fill();

	def clear(self):
		self.t.clear()