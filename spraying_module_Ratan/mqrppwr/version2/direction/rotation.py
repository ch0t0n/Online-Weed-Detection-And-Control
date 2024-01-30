import math

def dotproduct(p1, p2):
	return (p1[0]*p2[0]) + (p1[1]*p2[1])

def absolute(p):
	return math.sqrt((p[0]*p[0])+(p[1]*p[1]))

def rotation(p1, p2, p3):
	#p1->p2 is know direction and rotation towards p3
	d1 = (p2[0]-p1[0],p2[1]-p1[1])
	d2 = (p3[0]-p2[0],p3[1]-p2[1])
	#d1.d2
	d = dotproduct(d1, d2)
	theta = math.acos(d/(absolute(d1)*absolute(d2)))
	#angle
	theta1 = theta*(180.0/math.pi)
	return (round(theta,3), theta1)

def listofpoint(L):
	#assume L has more than 3 points
	R = []
	for i in range(len(L)-2):
		R.append(rotation(L[i], L[i+1], L[i+2]))
	return R

def distance(L):
	D = []
	for i in range(len(L)-2):
		d = math.sqrt(math.pow(L[i+1][0]-L[i+2][0],2) + math.pow(L[i+1][1]-L[i+2][1],2))
		D.append(round(d,3))
	return D
def cost(R, D):
	Total = 0.0
	for i in range(len(R)):
		Total += R[i][0]+D[i]
	return Total
#(A1,T1) -> (4,5,2,3)
#L = [(0,2), (0,3), (2,3), (0,5), (2,5), (4,4)]

#(A1,T1) -> (3,2,5,4)
#L = [(0,2), (0,3), (4,4), (2,5), (0,5), (2,3)]

#(A1,T2) -> (4,5,2,3)
#L = [(0,2), (0,3), (5,2), (5,0), (3,1), (1,1)]

#(A1,T2) -> (3,2,5,4)
#L = [(0,2), (0,3), (1,1), (3,1), (5,0), (5,2)]

#(A2,T1) -> (4,5,2,3)
#L = [(5,2), (5,3), (2,3), (0,5), (2,5), (4,4)]

#(A2,T1) -> (3,2,5,4)
L = [(5,2), (5,3), (4,4), (2,5), (0,5), (2,3)]

#(A2,T2) -> (4,5,2,3)
#L = [(5,2), (5,3), (5,2), (5,0), (3,1), (1,1)]

#(A2,T2) -> (3,2,5,4)
#L = [(5,2), (5,3), (1,1), (3,1), (5,0), (5,2)]

R = listofpoint(L)
D = distance(L)
Total = cost(R,D)
print R
print D
print Total

