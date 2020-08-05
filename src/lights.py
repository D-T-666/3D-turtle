from vector import *


class Point_light:
	def __init__(self, pos=Vector(), col=Vector(), val=1.):
		self.pos, self.col, self.val = pos, col, val

	def __getitem__(self, n):
		return self.pos

	def get_projected(self, distance=3):
		z = 1/(distance-self.pos.z)
		mat = np.array([[z, 0., 0.], [0., z, 0.], [0., 0., 1.]])
		return self.pos*mat