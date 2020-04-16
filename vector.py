import math
import numpy as np

class Vector:
	def __init__(self, x=0., y=0., z=0.):
		self.x, self.y, self.z = 0,0,0
		if type(x) == list or isinstance(x, np.ndarray):
			self.x = float(x[0])
			self.y = float(x[1])
			self.z = float(x[2])
		elif type(x) == int or type(x) == float:
			self.x = x
			self.y = y
			self.z = z
		else:
			raise TypeError('Vector can not be initialized with '+str(type(x)))

	def copy(self):
		return Vector(self.x, self.y, self.z)

	def magSq(self):
		return self.x**2+self.y**2+self.z**2

	def mag(self):
		return math.sqrt(self.magSq())

	def normalize(self):
		mag = self.mag()
		self.x /= mag
		self.y /= mag
		self.z /= mag
		return self

	def normalized(self):
		return self.copy().normalize()

	def setMag(self, val):
		self.normalize()
		self.x *= val
		self.y *= val
		self.z *= val
		return self

	def get_coords(self):
		return np.array([self.x, self.y, self.z])

	def rotateZ(self, a):
		s = np.sin(a)
		c = np.cos(a)
		rot_mat = np.array([[c,-s, 0],
							[s, c, 0],
							[0, 0, 1]])
		return Vector(rot_mat.dot(self.get_coords()))

	def rotateY(self, a):
		s = np.sin(a)
		c = np.cos(a)
		rot_mat = np.array([[ c, 0, s],
							[ 0, 1, 0],
							[-s, 0, c]])
		return Vector(rot_mat.dot(self.get_coords()))

	def rotateX(self, a):
		s = np.sin(a)
		c = np.cos(a)
		rot_mat = np.array([[1, 0, 0],
							[0, c,-s],
							[0, s, c]])
		return Vector(rot_mat.dot(self.get_coords()))

	def dot(self, other):
		dot  = self.x*other.x
		dot += self.y*other.y
		dot += self.z*other.z
		return dot

	def cross(self, other):
		nVec = Vector(self[1]*other[2]-self[2]*other[1],
					  self[2]*other[0]-self[0]*other[2],
					  self[0]*other[1]-self[1]*other[0])
		return nVec

	def norm_dot(self, other):
		nVec = self.normalized()
		oVec = other.normalized()
		dot  = nVec.x*oVec.x
		dot += nVec.y*oVec.y
		dot += nVec.z*oVec.z
		return dot

	def __add__(self, other):
		nVec = self.copy()
		nVec.x += other.x
		nVec.y += other.y
		nVec.z += other.z
		return nVec

	def __sub__(self, other):
		nVec = self.copy()
		nVec.x -= other.x
		nVec.y -= other.y
		nVec.z -= other.z
		return nVec

	def __mul__(self, other):
		if isinstance(other, np.ndarray):
			return Vector(other.dot(self.get_coords()))

		elif type(other) == int or type(other) == float:
			vec = self.copy()
			vec.x *= other
			vec.y *= other
			vec.z *= other
			return vec

		elif isinstance(other, Vector):
			return other.get_coords().dot(self.get_coords())
		
		else:
			raise TypeError('Vector can\'t be multiplied by '+str(type(other)))
	
	def __str__(self):

		return f'x: {self.x}\ny: {self.y}\nz: {self.z}\n';
	def __getitem__(self,ind):
		if ind == 0:
			return self.x
		if ind == 1:
			return self.y
		if ind == 2:
			return self.z
	def __setitem__(self,index,value):
		if ind == 0:
			self.x = value
		if ind == 1:
			self.y = value
		if ind == 2:
			self.z = value
	def __len__(self):
		return 3

	def average(vectors):
		vec = Vector()
		for v in vectors:
			vec += Vector(v[0], v[1], v[2])
		m = vec.mag()
		vec.setMag(m/len(vectors))
		return vec



def get_rotation_matrix(x=0,y=0,z=0):
	rot_mat = np.array([[1.0 if j == i else 0.0 for j in range(3)] for i in range(3)])
	# X
	if x != 0:
		rot_mat = rot_mat.dot([ [1,          0,           0],
								[0,  np.cos(x),  -np.sin(x)],
								[0,  np.sin(x),   np.cos(x)] ])
	# Y
	if y != 0:
		rot_mat = rot_mat.dot([ [np.cos(y),  0, -np.sin(y)],
								[        0,  1,          0],
								[np.sin(y),  0,  np.cos(y)] ])
	# Z
	if z != 0:
		rot_mat = rot_mat.dot([ [np.cos(z),  -np.sin(z),  0],
								[np.sin(z),   np.cos(z),  0],
								[        0,           0,  1] ])
	return rot_mat

def project(ps, distance=5):
	for i in range(len(ps)):
		z = 1/(distance-ps[i][2])

		mat = np.array([[z, 0., 0.], [0., z, 0.], [0., 0., 1.]])

		ps[i] = mat.dot(ps[i])

def distSq(p1, p2):
	return sum([n**2 for n in np.array(p1)-p2])


# -- test cases -- 
# everything works!!!! :D

# # test 1
# print(Vector())
# # test 2
# print(Vector(0,0,0))
# # test 3
# print(Vector(np.array([0,1,6])))
# # test 4
# v = Vector(np.array([0,1,6]))
# v *= np.array([[0,1,6], [-1, 2, 0], [-1, 2, 0]])
# print(v)
# # test 5
# v = Vector(np.array([0,0,4]))
# print(v.normalized())
# print(v)
# # test 6
# v.setMag(6)
# print(v)
# # test 7
# print(v.mag())
# print(v.magSq())
# # test 8
# print(Vector(2, 3, -1)[0])
# print(Vector(2, 3, -1)[1])
# print(Vector(2, 3, -1)[2])
# # test 9
# print(Vector(2, 3, -1).get_coords())
# # test 10
# print(Vector(Vector()))
# # test 11
# print(Vector()*'string')