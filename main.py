import random
import time
from vector import *
from mesh import *
import window
from lights import Point_light
import os

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
mesh.set_global_transform(Vector(0,0,0), Vector(0,0,0))
# mesh = Mesh(sys.argv[1])

class main:
	def __init__(self):
		# frame counter
		self.frame = 0
		# this is a class that wraps the turtle and turtle.screen
		self.canvas = window.Screen()
		# a vactor for keeping track of the mouse position
		self.mouse = Vector() # not implemented yet
		# a vector that holds the position of the camera
		self.camera = Vector(0, 0, 0) # camera movement and rotation not implemented yet
		# a variable that is used in the projection matrix calculations
		self.distance = 3
		# a variable that is used for upscaling the projected objects to the screen size
		self.scl = 800;
		# -- lights --
		# an array that holds different point lights
		self.lights = [] # you can have as many point lights as you want
		self.lights.append( Point_light( Vector(2, 2, 2), Vector(1,.95,.9), 2. ) )
		# self.lights.append( Point_light( Vector(2, 2, 2), Vector(1,.95,.9), 1. ) )
		# -- main loop --
		self.run()

	# event that needs to get called every time the mouse is dragged over the window
	def dragged(self, x, y):
		# last time I tried this with janky mouse input, it worked. but If you
		# have any improvement suggestions, please!
		mesh.rotation.x +=  (self.mouse.y-y/300.)
		mesh.rotation.y += -(self.mouse.x-x/500.)
		self.mouse = Vector(x/500, y/300, 0)

	# this method gets called preferably every frame
	def update(self):
		# increment the value of the frame counter variable
		self.frame+=1
		# rotate the mesh 1/100 of full rotation in the y axis (roll)
		mesh.transform(get_rotation_matrix(
			0, np.pi*2*0.01
		))

	# this method returns the position of the lights and the faces of the mesh
	# after projection
	def get_world_mesh(self):
		# copy the positions of the point lights to a new variable
		lights = [l.get_projected() for l in self.lights]
		# get projected faces of the mesh
		faces = mesh.get_projected_faces(self.distance)
		# filter the faces depending on their normal's Z value
		faces = [f for f in faces if f[3].z > 0]
		return (lights, faces)

	def draw_mesh_fast(self, shaded=True):
		# clear the bcakground and color it black
		self.canvas.bgcolor('black')
		self.canvas.clear()

		# get positions of lights and faces of the mesh
		lights, faces = self.get_world_mesh()
		# sort faces depending on their z value
		faces.sort(key=lambda a:(Vector.average(a[:3])-Vector(0, 0, -3)).magSq())
		# loop ofer faces
		for f in faces:
			# get the ilumination of the face
			shade_col = tuple(self.get_face_color(f, lights)) if shaded else (255,255,255)
			# get the background color of the canvas
			bg_col = self.canvas.bgcolor()

			# set fill and stroke colors
			self.canvas.fill(		shade_col		)
			self.canvas.stroke(		shade_col		)

			# command the canvas to draw the face with the specified parameters
			self.canvas.drawPolygon(f[:-2], self.scl, stroke=True, fill=True)

		# update the canvas
		self.canvas.update()
		# update the objects
		self.update()

	def get_face_color(self, face, lights):
		# get the original color of the face and than un-normalize it
		shade_col = face[-1]*127

		# loop over every point light
		for light in self.lights:
			light_pos = light.get_projected()
			# get the dot product of the normal of the face and the direction of
			# the light from the face
			dot = float((light_pos-face[0]).norm_dot(face[-2]))
			# if the normal of the face is facing more than π/2, light shouldn't
			# illuminate the face
			if dot > 0:
				# get the inverse square of the distance from the face to the poin light
				d = 1/distSq(face[0],light_pos)
				# add the color of the light multiplied by the iverse of the distance to
				# the point light and the dot
				shade_col += (light.col*float(d))*((dot*.5+.5)*light.val*255)

		# turn the color vector into a int vector and limit it from 0 to 255
		col = [*map(lambda a:min(max(0, int(a)), 255),shade_col.get_coords())]
		# return a tuple of the color
		return (col[0], col[1], col[2])

	# main loop
	def run(self):
		# I don'n run the loop infinitley because in the case of an error,
		# I wan't the program to finish by itself, even if it takes a long time
		for i in range(1000):
			# start the timer
			st = time.time()
			# run the draw function
			self.draw_mesh_fast(shaded=True)
			# stop the timer
			et = time.time()
			# print the fps
			print('FPS = '+str(round(1/(et-st)*100)/100),end='\r')

# run the main environment
m = main();