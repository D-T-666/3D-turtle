import numpy as np
import random
import turtle
import time
from vector import *
from mesh import *
import os

true = True
false = False

os.system('cls')


def makeTree(m, pos=Vector(0, -2, 0), size=2, a=0, f=0):
	p = pos.copy()
	p1 = p+Vector( size/10, size*.2, -size/10).rotateZ(a).rotateX(f).rotateY(np.pi/4 if size == 2 else 0);
	p2 = p+Vector(-size/10, size*.2, -size/10).rotateZ(a).rotateX(f).rotateY(np.pi/4 if size == 2 else 0);
	p3 = p+Vector(-size/10, size*.2,  size/10).rotateZ(a).rotateX(f).rotateY(np.pi/4 if size == 2 else 0);
	p4 = p+Vector( size/10, size*.2,  size/10).rotateZ(a).rotateX(f).rotateY(np.pi/4 if size == 2 else 0);
	p5 = p+Vector(       0,    size,        0).rotateZ(a).rotateX(f).rotateY(np.pi/4 if size == 2 else 0);
	p6 = p+Vector(       0,       0,        0).rotateZ(a).rotateX(f).rotateY(np.pi/4 if size == 2 else 0);
	m.verts.append(p1)
	m.verts.append(p2)
	m.verts.append(p3)
	m.verts.append(p4)
	m.verts.append(p5)
	m.verts.append(p6)
	m.faces.append([m.verts.index(p1)+1, m.verts.index(p2)+1, m.verts.index(p5)+1])
	m.faces.append([m.verts.index(p2)+1, m.verts.index(p3)+1, m.verts.index(p5)+1])
	m.faces.append([m.verts.index(p3)+1, m.verts.index(p4)+1, m.verts.index(p5)+1])
	m.faces.append([m.verts.index(p4)+1, m.verts.index(p1)+1, m.verts.index(p5)+1])
	m.faces.append([m.verts.index(p2)+1, m.verts.index(p1)+1, m.verts.index(p6)+1])
	m.faces.append([m.verts.index(p3)+1, m.verts.index(p2)+1, m.verts.index(p6)+1])
	m.faces.append([m.verts.index(p4)+1, m.verts.index(p3)+1, m.verts.index(p6)+1])
	m.faces.append([m.verts.index(p1)+1, m.verts.index(p4)+1, m.verts.index(p6)+1])

	pos=pos+Vector(      0, size, 0).rotateZ(a).rotateX(f);
	if size > 0.8:
		makeTree(m, pos, size/1.8, a, f+np.pi*0.257)
		makeTree(m, pos, size/1.8, a, f-np.pi*0.257)
		makeTree(m, pos, size/1.8, a+np.pi*0.257, f)
		makeTree(m, pos, size/1.8, a-np.pi*0.257, f)


mesh = Mesh()
def run():
	path = '3d files/'
	extension = '.obj'
	objects = [
		'teapot',
		'dt6',
		'penguin',
		'sword',
		'sword1',
		'suzanne',
		'ufo',
		'computer with materials'
	]
	print('choose a 3D object to display:')
	for i in range(len(objects)):
		print(f' [ {i} ]  {objects[i]}')
	# print()
	choice = '~'#'1' #
	while not choice in [*map(str,range(len(objects)))]:
		if choice != '~':
			print('please input a number.')
		choice = input('> ');
	mesh.loadMesh('3d files/'+objects[int(choice)]+'.obj')
run()
mesh.set_global(Vector(0,0,0), Vector(0,0,0))
# mesh = Mesh()
# makeTree(mesh)
# rotate_points
# mesh = Mesh('3d files/teapot.obj')
# mesh = Mesh('3d files/dt6.obj')
# mesh.transform(get_rotation_matrix(
# 	np.pi*2*0.25
# 	))
# mesh = Mesh('3d files/penguin.obj')
# mesh = Mesh('3d files/sword.obj')
# mesh = Mesh('3d files/sword1.obj')
# mesh.transform(get_rotation_matrix(0, np.pi/2))
# mesh = Mesh('3d files/cubetree.obj')
# mesh = Mesh('3d files/suzanne.obj')
# mesh = Mesh('3d files/ufo.obj')
# mesh = Mesh('3d files/computer with materials.obj')
# mesh.translate(np.array([
# 	[0.75,0,0,0.35],
# 	[0,0.75,0,0],
# 	[0,0,0.75,0]
# ]))
# mesh = Mesh(sys.argv[1])

class main:
	def __init__(self):

		self.setup();
	def setup(self):
		self.frame = 0
		self.screen = turtle.Screen()
		self.screen.setup(600, 600)
		self.screen.colormode(255)
		self.t = turtle.Turtle()
		self.t.speed(0)
		self.t.up()
		self.t.ht();
		self.screen.tracer(0)

		self.mouse = Vector()

	# -- camera --
		self.camera = Vector(0, 0, 0)
		self.distance = 3
		self.scl = 800;
	# -- lights -- 
		self.lights = np.array([[2., 2., 2.]])#, [-2., 2., 2.]])
		self.light_colors = np.array([[252., 171., 106.]])#,[0., 100., 100.]])
	# -- main loop --

		turtle.ondrag(self.dragged)
		self.screen.listen()
		self.run()

	def dragged(self, x, y):
		print(x, y)
		mesh.rotation.x +=  (self.mouse.y-y/500.)
		mesh.rotation.z += -(self.mouse.x-x/500.)
		self.mouse = Vector(x/500, y/500, 0)

	def update(self):
		self.frame+=1
		mesh.transform(get_rotation_matrix(
			0, np.pi*2*0.01
			))
		pass

	def get_world_mesh(self):
		lights = self.lights[:]
		project(lights, self.distance)
		# getting faces from every mesh
		faces = mesh.get_faces(self.distance)
		# filtering every mesh separatley
		faces = [f for f in faces if f[3].z > 0]
		return (lights, faces)


	def draw_mesh_fast(self, shaded=True):
		self.background('black')
		self.t.clear()

		lights, faces = self.get_world_mesh()
		faces.sort(key=lambda a:(Vector.average(a[:3])-Vector(0, 0, -3)).magSq())
		for f in faces:
			shade_col, bg_col = tuple(self.get_face_color(f, lights)) if shaded else (255,255,255), self.t.screen.bgcolor()

			fill_col = shade_col
			stroke_col = bg_col

			self.t.color(stroke_col,fill_col)
			self.drawFace(f, stroke=False, fill=True)
		self.t.screen.update()
		self.update()

	def get_face_color(self, face, lights):
		shade_col = face[-1]*127

		for i in range(len(lights)):
			dot = float((Vector(self.lights[i])-face[0]).norm_dot(face[-2]))
			if dot > 0:
				d = 1/distSq(face[0].get_coords(),lights[i])
				shade_col += (Vector(self.light_colors[i])*float(d))*(dot+1.)

		col = [*map(lambda a:min(max(0, int(a)), 255),shade_col.get_coords())]
		return (col[0], col[1], col[2])
			

	def stroke(self, col):
		self.t.pencolor(col)

	def fill(self, col):
		self.t.fillcolor(col)

	def background(self, col):
		self.screen.bgcolor(col)

	def drawFace(self, face, stroke=False, fill=True):
		self.t.goto(face[0][0]*self.scl, face[0][1]*self.scl)
		if fill: self.t.begin_fill();
		if stroke: self.t.down();
		for i in range(1,len(face)-2):
			self.t.goto(face[i][0]*self.scl, face[i][1]*self.scl)
		self.t.goto(face[0][0]*self.scl, face[0][1]*self.scl)
		if stroke: self.t.up();
		if fill: self.t.end_fill();

	def run(self):
		for i in range(10000):
			st = time.time()
			self.draw_mesh_fast(shaded=True)
			et = time.time()
			print('FPS = '+str(round(1/(et-st)*100)/100),end='\r')

m = main();