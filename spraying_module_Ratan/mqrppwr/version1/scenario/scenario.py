import configparser
import json
import numpy

def scenario_reader(filePath):
	"""
	input: path of input file
	output: S = (I, Q, T, D, W, C)
		I - list of positions for infected plants
		Q - list of drone's positions
		T - list of tank's position
		D - dictionary {q1:d1,...} (q1,d1) express the direction
		W - dictionary{i1:c1, ....} c1 is the amount of infection
						 at plant's position i1
		C - maximum amount of pesticide that drone can carry
	"""
	inifile = configparser.ConfigParser()
	inifile.read(filePath, 'UTF-8')

	infectedLocations = json.loads(inifile.get('settings', 'infectedLocations'))
	I = []
	for v in infectedLocations:
		I.append((v[0],v[1]))
	infectedAmount = json.loads(inifile.get('settings', 'infectedAmount'))
	Ia = []
	for v in infectedAmount:
		Ia.append(v)

	droneLocations = json.loads(inifile.get('settings', 'droneLocations'))    
	Q = []
	for v in droneLocations:
		Q.append((v[0],v[1]))

	tankLocations = json.loads(inifile.get('settings', 'tankLocations'))
	T = []
	for v in tankLocations:
		T.append((v[0],v[1]))

	droneDirections = json.loads(inifile.get('settings', 'droneDirections'))
	DQ = []
	for v in droneDirections:
		DQ.append((v[0],v[1]))

	D = dict()
	for i in range(len(Q)):
		D[Q[i]] = DQ[i]

	W = dict()
	for i in range(len(I)):
		W[I[i]] = Ia[i]
	
	C = 0
	C = inifile.getint('settings', 'droneCarry')

	#scenario
	S = (I, Q, T, D, W, C)
	return S
    
    
    
