import math

def get_key(D, v):
	"""
	input: 
		D - dictionary
		v - value
	output:
		k - key for the value v in D
	"""
	
	L = [key for key,value in D.items() if v==value]
	if len(L)>0:
		return L[0]
	else:
		return -1


def get_validedges(Node_dict):
	"""
	
	"""
	f = open("./milp/model.sol", "r")
	contents = f.readlines()
	f.close()
	Edge_dict = {}
	first = True
	for line in contents:
		if first==True:
			first = False
		else:
			expr = line.strip('\n').split(' ')	
			value = math.ceil(float(expr[1]))
			expr = expr[0].split('_')
			source = get_key(Node_dict, int(expr[1]))
			target = get_key(Node_dict, int(expr[2]))
			if value != 0.0:
				Edge_dict[(source, target)] = value
	return Edge_dict

def get_path(Edge_dict, q):
	"""
	input: 	
		Edge_dict - dictionary of edges
		q - quadrotor node
	output:
		path - list of positions for quadrotor q
	"""
	path = []
	path.append(q)
	current = q
	#print(Edge_dict)
	while True:
		point_lst = [e[1] for e in Edge_dict.keys() if e[0]==current]
		#print("Points")
		#print(point_lst)
		if len(point_lst)!=1 or point_lst[0] in path:
			break
		else:
			path.append(point_lst[0])
			current = point_lst[0]
	return path[:-1]
			
	

def extract_paths(G, Node_dict):
	"""
	input:
		G - a directed graph
		Node_dict - mapping between node and gurobi variables

	"""
	Edge_dict = get_validedges(Node_dict)
	Q = [q for q in G.nodes() if G.node[q]['kind']==0]
	paths = {}
        
	for q in Q:
		#print("Loop")
		path = get_path(Edge_dict, q)
		paths[q] = path
	return paths

		
	
	
