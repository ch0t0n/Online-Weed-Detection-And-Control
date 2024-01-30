import random
import os

def create_scenario(Q, I, T, D, C, filename):
	"""
	
	"""
	f = open(filename, "w")
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
	while i < Nd[0]: 
		#print(i)
		x = round(random.uniform(xl, xu), digits)
		y = round(random.uniform(yl, yu), digits)
		#print(x)
		#print(y)
		if not([x,y] in Q):
			Q.append([x,y])
			i = i+1
		else:
			continue

	# initial direction for drones
	D = []
	i = 0
	while i < Nd[0]: 
		x = round(random.uniform(xl, xu), digits)
		y = round(random.uniform(yl, yu), digits)
		D.append([x,y])
		i = i+1
		
	# number of plants positions
	I = []
	i = 0
	while i < Np[0]: 
		#print(i)
		x = round(random.uniform(xl, xu), digits)
		y = round(random.uniform(yl, yu), digits)
		if not([x,y] in Q) and not([x,y] in I):
			I.append([x,y])
			i = i+1
		else:
			continue

	# number of tank positions
	T = []
	i = 0
	while i < Nt[0]: 
		#print(i)
		x = round(random.uniform(xl, xu), digits)
		y = round(random.uniform(yl, yu), digits)
		if not([x,y] in Q) and not([x,y] in I) and not([x,y] in T):
			T.append([x,y])
			i = i+1
		else:
			continue

	for j in range(len(Nt)-1):
		filename = str(len(Q))+'-'+str(len(I))+'-'+str(len(T))+'.ini'
		if j==0:	
			create_scenario(Q, I, T, D, C, filename)
		i = 0
		while i < Nt[j+1]-Nt[j]: 
			#print(i)
			x = round(random.uniform(xl, xu), digits)
			y = round(random.uniform(yl, yu), digits)
			if not([x,y] in Q) and not([x,y] in I) and not([x,y] in T):
				T.append([x,y])
				#x = round(random.uniform(xl, xu), digits)
				#y = round(random.uniform(yl, yu), digits)
				#D.append([x,y])
				i = i+1
			else:
				continue
		filename = str(len(Q))+'-'+str(len(I))+'-'+str(len(T))+'.ini'
		create_scenario(Q, I, T, D, C, filename)
		

#(xl, xu, yl, yu, Nd, Np, Nt, C)
random_config(0,25,0,25,[5],[50],[5,10,15,20,25], 5)

	
	
