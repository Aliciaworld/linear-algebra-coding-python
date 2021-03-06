from math import sqrt, acos, pi
from decimal import Decimal  #to give the better numerical precision#
from decimal import getcontext

getcontext().prec = 30

class Vector(object):
	def __init__(self, coordinates): #create a vector based on an input list of coordinates#
		try:
			if not coordinates:
				raise ValueError
			self.coordinates = tuple([Decimal(x) for x in coordinates])
			self.dimension = len(coordinates)  #set the dimension of space that the vector lives in#
		except ValueError:
			raise ValueError('The coordinates must be nonempty')		
		except TypeError:
			raise TypeError('The coordinates must be an iterable')
	
	def __str__(self):  #print out the coordinates of the vector using python's built in print function#
		return 'Vector:{}'.format(self.coordinates)	

	
	def __eq__(self, v):  #to test whether two vectors are equal#
		return self.coordinates == v.coordinates
		#如果不实现__eq__方法，自定义类型会调用默认的__eq__方法，通过默认方法进行比较的相等条件相当严格，只有自己和自己比才会返回True，因此，建议需要进行自定义类型比较的时候，实现__eq__方法#
	
	def plus(self, v):
		new_coordinates=[x+y for x, y in zip(self.coordinates, v.coordinates)]
		return Vector(new_coordinates)	
		#也可以直接return [x+y for x, y in zip(self.coordinates, v.coordinates)]
	
	def minus(self, v):
		new_coordinates = [x-y for x, y in zip(self.coordinates, v.coordinates)]
		return Vector(new_coordinates)
		
	def times_scalar(self, c):
		new_coordinates = [c*x for x in self.coordinates]
		return Vector(new_coordinates)
	
	def magnitude(self):
		coordinates_squared=[X**2 for X in self.coordinates]
		return sqrt(sum(coordinates_squared))

	def normalized(self):
		try:
			magnitude=self.magnitude()  #调用前面的函数magnitude#
			return self.times_scalar(Decimal('1.0')/magnitude)  #调用前面的函数times_scalar#		
		except ZeroDivisionError:
			raise Exception('Cannot normalize the zero vector')				
	
	def dot(self, v):
		return sum([x*y for x, y in zip(self.coordinates, v.coordinates)])

	def angle_with(self, v, in_degrees=False):  #in_degrees=False是缺省设置，如果是True下面的if in_degrees会work#
		try:
			u1 = Vector(self.normalized())  #将归一化的list转为Vector,否则下面的dot无法进行#
			u2 = Vector(v.normalized())
			angle_in_radians = acos(u1.dot(u2))
			#上面三行比较烧脑，也可以将这三行写成angle_in_randians = acos(self.dot(v)/self.magnitude()/v.magnitude()
			if in_degrees:
				degrees_per_radian = 180./pi
				return angle_in_radians * degrees_per_radian
			else:
				return angle_in_radians
		except Exception as e:
			if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
				raise Exception('Cannot compute an angle with the zero vector')
			else:
				raise e

	def is_orthogonal_to(self, v, tolerance=1e-10):
		return abs(self.dot(v))< tolerance
	# due to the precision issues, have to check the dot product has a very small absolute value#
	
	def is_zero(self, tolerance=1e-10):
		return self.magnitude() < tolerance	
	
	def is_parallel_to(self, v):
		return (self.is_zero() or v.is_zero() or self.angle_with(v) == 0 or self.angle_with(v) == pi)

#the projection of a vector onto a basis vector is found by first normalizing the basis vector to form a unit vector u. Then, taking the dot product of u, with the vector we're projecting. And then multiplying u by the result of the dot product.#
# we should consider if the basis vector is zero#	
	
	def component_parallel_to(self, basis):
		try:
			u = basis.normalized()
			weight = self.dot(u)
			return u.times_scalar(weight)
	
		except Exceptiong as e:
			if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
				raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
			else:
				raise e
	
	def component_orthogonal_to(self, basis):
		try:
			projection = self.component_parallel_to(basis)
			return self.minus(projection)
		except Exception as e:
			if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
				raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
			else:
				raise e
	
	def cross(self, v):
		try:
			x_1, y_1, z_1 = self.coordinates
			x_2, y_2, z_2 = v.coordinates
			new_coordinates = [y_1*z_2 - y_2*z_1,
							 -(x_1*z_2 - x_2*z_1),
							   x_1*y_2 - x_2*y_1]
			return Vector(new_coordinates)
		except ValueError as e:
			msg = str(e)
			if msg == 'need more than 2 values to unpack':
				self_embedded_in_R3 = Vector(self.coordinates + ('0',))
				v_embedded_in_R3 = Vector(v.coordinates + ('0',))
				return self_embedded_in_R3.cross(v.embedded_in_R3)
			elif (msg == 'too many values to unpack' or 
				  msg == 'need more than 1 values to unpack'):
				raise Exception(self.ONLY_Defined_IN_TWO_THREE_DIMS_MSG)
			else:
				raise e
	
		
	def area_of_parallelogram_with(self, v)：
		cross_product = self.cross(v)
		return cross_product.magnitude()
	
	def area_of_triangle_with(self, v):
		return self.area_of_parallelogram_with(v) / Decimal('2.0')

#for example#
v = Vector([8, 9])
w = Vector([3, 7])
c = 1.5
print (v.plus(w))
print (v.magnitude())
print (v.normalized())
print (v.minus(w))
print (v.times_scalar(c))

#output#
Vector: (11, 16)
Vector: (5, 2)
Vector: (12, 13.5)

...

	
	
