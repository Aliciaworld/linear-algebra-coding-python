from decimal import Decimal, getcontext

from vector import Vector  #make use of the Vector class from the previous lesson#

getcontext().prec = 30

class Line(object):
	NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

#the init took two piece of information:a normal vetor to the line and the constant term for the lines equation#
#normal vector gives the coefficients for the standard form of the line#
	def __init__(self, normal_vector = None, constant_term = None):
		self.dimension = 2
		
		if not normal_vector:
			all_zeros = ['0']*self.dimension
			normal_vector = Vector(all_zeros)
		self.normal_vector = normal_vector	
	
		if not constant_term:
			constant_term = Decimal('0')
		self.constant_term = Decimal(constant_term)
		self.set_basepoint()
	
	def set_basepoint(self):
        try:
            n = self.normal_vector
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension

            initial_index = Line.first_nonzero_index(n)
            initial_coefficient = n[initial_index]

            basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e

#the str function outputs the standard form of the lines equation using the variable x1 and x2 instead of just x and y#
	def __str__(self):
		
		num_decimal_places = 3
		
		def write_coefficient(coefficient, is_initial_term = False):
			coefficient = round(coefficient, num_decimal_places)
			if coefficient % 1 == 0:
				coefficient = int(coefficient)
			output = ''
			if coefficient < 0:
				output += '-'
			if coefficient > 0 and not is_initial_term:
				output += '+'
			if not is_initial_term:
				output += ' '
			if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output

#make a defination: two lines are parallel,if their normal vectors are parallel#

	def is_parallel_to(self,ell):
		n1 = self.normal_vector
		n2 = ell.normal_vector
		return n1.is_parallel_to(n2)

# we check whether two parallel lines are equal by picking one point from each line and looking at the vector connecting them. If that vector is orthogonal to the normal vectors of both lines, then the two lines are equal.#
	def __eq__(self, ell):

# these code is to deal with the technical case that the normal vector of a line is the zero vector, which means the left hand side of the equation	defning the line is zero, since the coefficient of each variable is zero.#	
		if self.normal_vector.is_zero():
			if not ell.normal_vector.is_zero():
				return False
			else:
				diff = self.constant_term - ell.constant_term
				return MyDecimal(diff).is_near_zero()
		elif ell.normal_vector.is_zero():
			return False

#First, check the two lines being compared are parallel. If not then there's no chance of there being equal#			
		if not self.is_parallel_to(ell):
			return False
			
#Second,compute the vector connecting the two lines base points#		
		x0 = self.basepoint
		y0 = self.basepoint
		basepoint_difference = x0.minus(y0)

#Finally, check whether that vector is orthogonal to the normal vector of the first line.#
		n = self.normal_vector
		return basepoint_difference.is_orthogonal_to(n)
	
	def intersection_with(self, ell):
		try:
			A, B = self.normal_vector.coordinates
			C, D = ell.normal_vector.coordinates
			K1 = self.constant_term
			K2 = ell.constant_term
			
			x_numerator = D*k1 - B*k2
			y_numerator = -C*K1 + A*k2
			one_over_denom = Decimal('1')/(A*D - B*C)
			
			return Vector([X_numerator, y_numerator]).time_scalar(one_over_denom)
		
		 except ZeroDivisionError:
		 	if self == ell:
				return self
			else:
				return None


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps
		
#for example:
ell1 = line(normal_vector=Vector(['1.23', '2.22']), constant_term = '2.33')
ell1 = line(normal_vector=Vector(['4.23', '5.34']), constant_term = '1.23')
print 'intersection 1:', ell1.intersection_with(ell2)
