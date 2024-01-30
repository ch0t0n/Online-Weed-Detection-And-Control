import math

def dotproduct(p1, p2):
	"""
	input:
		p1 - a 2D point
		p2 - a 2D point
	output: d - dot product of p1 and p2
	"""
	d = (p1[0]*p2[0]) + (p1[1]*p2[1])
	return d

def absolute(p):
	"""
	input: p - a 2D point
	output:
		absp - absolute value of p
	"""
	#print(p)
	absp = math.sqrt((p[0]*p[0])+(p[1]*p[1]))
	#print(absp)
	return absp

def rotation(p1, p2, p3):
	"""
	input:
		p1 - a 2D point
		p2 - a 2D point
		p3 - a 2D point
	output:
		theta - rotation between p2-p1 and p3-p2
		in radian
	"""
	#p2-p1
	d1 = (p2[0]-p1[0],p2[1]-p1[1])
	#p3-p2
	d2 = (p3[0]-p2[0],p3[1]-p2[1])
	#d1.d2 
	d = dotproduct(d1, d2)
	#theta
	if absolute(d1)==0.0 or absolute(d2)==0.0:
		return 0.0
	theta = math.acos(d/(absolute(d1)*absolute(d2)))
	return round(theta,3)

def distance(p1, p2):
	"""
	input: 
		p1 - a 2D point
		p2 - a 2D point
	output:
		d - distance
	"""
	dist = math.sqrt(math.pow(p1[0]-p2[0],2) + math.pow(p1[1]-p2[1],2))
	return round(dist,3)

def rot_cost(p1, p2, p3, omega):
	"""
	input: 
		p1 - a 2D point
		p2 - a 2D point
		p3 - a 2D point
		omega - angular speed
	output:
		cr - cost of rotation
	"""
	theta = rotation(p1, p2, p3)
	cr = theta/omega
	return round(cr,3)

def dist_cost(p1, p2, vl):
	"""
	input:
		p1 - a 2D point
		p2 - a 2D point
		vl - linear speed
	output:
		ct - cost of travelling
	
	"""
	dist = distance(p1, p2)
	ct = dist/vl

	return round(ct,3)

def edge_cost(p1, p2, p3, omega, vl):
	"""
	input: 
		p1 - a 2D point
		p2 - a 2D point
		p3 - a 2D point
		omega - angular speed
		vl - linear speed
	output:
		ce - cost of edge
	"""
	cr =rot_cost(p1, p2, p3, omega)
	ct = dist_cost(p1, p2, vl)
	return round(cr+ct,3)
	

