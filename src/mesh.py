from vector import *

class Mesh:
	def __init__(self, file=False):
		self.verts = []
		self.faces = []
		self.colors = []

		self.position = Vector()
		self.rotation = Vector()

		if file!=False:
			self.loadMesh(file)
		
		self.verts = self.get_projected()
		# print(self.faces)
		# print(self.verts)

	def set_global_transform(self, position=Vector(), rotation=Vector()):
		self.position = position
		self.rotation = rotation

	def loadMesh(self, file_name):
		with open(file_name, 'r') as f:
			material_name = ''
			mtl = ''
			col_id = -1
			for l in f:
				if l[0] == 'v' and l[1] == ' ':
					a=Vector([*map(float,l[2:].split())])
					self.verts.append(a)
				if l[0] == 'f':
					a=[*map(int,l[2:].replace('//', ' ').split())]
					a.append(col_id)
					self.faces.append(a)
				if l[:6] == 'usemtl':
					col_line = mtl[(int(l[7])-1)*10+3]
					self.colors.append(Vector(col_line.split()[1:]))
					col_id += 1
				if l[:6] == 'mtllib':
					with open('3d files/'+l[7:-1], 'r') as mtl_file:
						mtl = [*mtl_file]
						mtl = mtl[3:]
			if col_id == -1:
				self.colors.append(Vector(0.5,0.5,0.5))

	def transform(self, mat):
		self.verts = [v*mat for v in self.verts]

	def translate(self, mat):
		self.verts = [Vector(mat.dot(list(v.get_coords())+[1])) for v in self.verts]
	
	def get_rotated(self):
		verts = self.verts[:]
		verts = [v.rotateX(self.rotation.x) for v in verts]
		verts = [v.rotateY(self.rotation.y) for v in verts]
		verts = [v.rotateZ(self.rotation.z) for v in verts]
		return verts

	def get_projected(self, distance=5):
		verts = self.get_rotated()
		verts = [(v+self.position) for v in verts]

		for i in range(len(verts)):
			z = 1/(distance-verts[i][2])

			mat = np.array([[z, 0., 0.], [0., z, 0.], [0., 0., 1.]])

			verts[i] = mat.dot(verts[i].get_coords())
		return verts

	def get_projected_faces(self, distance):
		verts = []
		if distance > 0:
			verts = self.get_projected(distance)
		else:
			verts = self.verts[:]
		faces = []
		for i in range(len(self.faces)):
			l1 = (verts[self.faces[i][1]-1]-verts[self.faces[i][0]-1])
			l2 = (verts[self.faces[i][2]-1]-verts[self.faces[i][0]-1])
			norm = Vector([l1[1]*l2[2]-l1[2]*l2[1],
						   l1[2]*l2[0]-l1[0]*l2[2],
						   l1[0]*l2[1]-l1[1]*l2[0]])

			face = []
			for j in range(len(self.faces[i])-1):
				face.append(Vector(verts[self.faces[i][j]-1]))
			face.append(norm)
			face.append(self.colors[self.faces[i][-1]])

			faces.append(face)
			
		return faces