import random
import os
import math

def create_scenario(Q, I, T, D, C):
	"""
	
	"""
	f = open("./configuration/config.ini", "w")
	f.write("[settings]"+"\n")
	f.write("infectedLocations = "+str(I)+"\n")
	f.write("droneLocations = "+str(Q)+"\n")
	f.write("tankLocations = "+str(T)+"\n")
	f.write("droneDirections = "+ str(D)+"\n")
	Ia = []
	for i in range(len(I)):
		Ia.append(random.randint(1,C))
	f.write("infectedAmount = "+str(Ia)+"\n")
	f.write("droneCarry = "+str(C))
	f.close()
	
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

def is_safe(x, y, Q):
	for q in Q:
		if distance([x,y], q)<1.0:
			return False
	return True

def random_config(xl, xu, yl, yu, Nd, Np , Nt, C):
	"""
	input:
		xl - lower bound of x-coordinates
		xu - upper bound of x-coordinates
		yl - lower bound of x-coordinates
		yu - upper bound of y-coordinates
		Nd - number of drones
		Np - number of plants
		Nt - number of tanks
		C - maximum capacity 
	"""
	
	digits = 5
	# number of drone positions
	Q = []
	i = 0
	while i < Nd: 
		#print(i)
		x = round(random.uniform(xl, xu), digits)
		y = round(random.uniform(yl, yu), digits)
		#print(x)
		#print(y)
		if not([x,y] in Q) and is_safe(x,y, Q):
			Q.append([x,y])
			i = i+1
		else:
			continue

	# initial direction for drones
	D = []
	i = 0
	while i < Nd: 
		x = round(random.uniform(xl, xu), digits)
		y = round(random.uniform(yl, yu), digits)
		D.append([x,y])
		i = i+1
		
	# number of plants positions
	I = []
	i = 0
	while i < Np: 
		#print(i)
		x = round(random.uniform(xl, xu), digits)
		y = round(random.uniform(yl, yu), digits)
		if not([x,y] in Q) and not([x,y] in I) and is_safe(x,y,Q) and is_safe(x,y, I):
			I.append([x,y])
			i = i+1
		else:
			continue

	# number of tank positions
	T = []
	i = 0
	while i < Nt: 
		#print(i)
		x = round(random.uniform(xl, xu), digits)
		y = round(random.uniform(yl, yu), digits)
		if not([x,y] in Q) and not([x,y] in I) and not([x,y] in T) and is_safe(x,y,Q) and is_safe(x,y, I) and is_safe(x,y, T):
			T.append([x,y])
			i = i+1
		else:
			continue


	create_scenario(Q, I, T, D, C)

#(xl, xu, yl, yu, Nd, Np, Nt, C)
random_config(0,25,0,25,10,50,15, 5)

	
	
