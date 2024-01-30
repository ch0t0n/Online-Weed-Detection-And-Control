import math
import random
from gurobipy import *
import networkx as nx

# Callback - use lazy constraints to eliminate sub-tours
def subtourelim(model, where):
	try:
		if where == GRB.callback.MIPSOL:
			selected = []
			# make a list of edges selected in the solution

			E = G.edges()
			sol = model.cbGetSolution([model._vars[E_dict[E[i]][0],E_dict[E[i]][1]] for i in range(len(E))])
		
			selected = [(E_dict[E[i]][0],E_dict[E[i]][1]) for i in range(len(E)) if sol[i] == 1 and not(G.node[E[i][0]]['kind']==3 or G.node[E[i][1]]['kind']==3)]
		
			# find the shortest cycle in the selected edge list
			tour = subtour(selected)
			print(tour)
			
			if len(tour) > 1:
				expr= 0
				for i in range(len(tour)-1):
					expr += model._vars[tour[i], tour[i+1]]	
				model.cbLazy(expr <= len(tour)-1)

	except GurobiError:
        	print ('Error reported')

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


# Given a list of edges, finds the shortest subtour

def subtour(edges):
	source = [e[0] for e in edges]
	target = [e[1] for e in edges]
	nodes = list(set(source+target))
	visited = {}
	for node in nodes:
		visited[node] = False
	cycles = []
	lengths = []
	selected = {}
	for e in edges:
		selected[e[0]] = [e[1]]
	#many cases needs to be considered
	#(a) v1->v2 (v2 may be visited first)
	#(b) v1 may not be visited and do not have neighbours
	while True:
		current = get_key(visited, False)
		if current == -1:
			break
		thiscycle = [current]
		iscycle=True
		while True:
			visited[current] = True
			if current in selected.keys():
				neighbors = [x for x in selected[current] if not visited[x]]
				if len(neighbors) == 0:
					break
			else:
				iscycle=False
				break
			current = neighbors[0]
			thiscycle.append(current)
		if iscycle==True and current == thiscycle[0] and len(thiscycle)>1:
			cycles.append(thiscycle)
			lengths.append(len(thiscycle))
		
	if len(cycles)==0:
		thiscycle = []
		cycles.append(thiscycle)
		lengths.append(len(thiscycle))
	
	return cycles[lengths.index(min(lengths))]



def optimization(G1, dummy):
	"""

	"""
	global G
	G = G1.copy()
	
	Node_dict = {}
	i = 1
	for node in G.nodes():
		Node_dict[node] = i
		i = i+1
	
	#create a model
	m = Model()

	#create all edges
	E = G.edges()
	
	# mapping between edge and unique number
	global E_dict
	E_dict = {}
	for e in E:
		E_dict[e] = (Node_dict[e[0]], Node_dict[e[1]])
		
	
	#create variables
	vars = {}

	for i in range(len(E)):
		vars[E_dict[E[i]][0], E_dict[E[i]][1]] = m.addVar(obj=G[E[i][0]][E[i][1]]['cost']+G.node[E[i][1]]['cost'], vtype=GRB.BINARY, name='e_'+str(E_dict[E[i]][0])+'_'+str(E_dict[E[i]][1]))
	m.update()

	# All nodes 
	Q = [q for q in G.nodes() if G.node[q]['kind']==0]
	I = [p for p in G.nodes() if G.node[p]['kind']==1]
	T = [t for t in G.nodes() if G.node[t]['kind']==2]
	E = G.edges()
	#number of outdegree from dummy node is equal to the number of drones
	Q = [q for q in G.nodes() if G.node[q]['kind']==0]

	m.addConstr(quicksum(vars[E_dict[(dummy,q)][0], E_dict[(dummy,q)][1]] for q in Q)== len(Q))

	#number of indegree to dummy node is equal to the number of drones
	m.addConstr(quicksum(vars[E_dict[(q,dummy)][0], E_dict[(q,dummy)][1]] for q in Q+I)== len(Q))
	
	#Indegree and out degree of each node except dummy node is the same
	for p in I+Q+T:
		#indegree for plant
		m.addConstr(quicksum(vars[E_dict[(v1,v2)][0], E_dict[(v1,v2)][1]] for (v1,v2) in E if v2==p) - quicksum(vars[E_dict[(v1,v2)][0],E_dict[(v1,v2)][1]] for (v1,v2) in E if v1==p)==0)

	#indegree to the group of nodes having same id is 1
	# set of ids for plants
	
	Ids = list(set([G.node[p]['cid'] for p in I]))
	
	#f = open("temp.txt", "w")
	#f.write(str(E))

	for i in range(len(Ids)):
		ids = Ids[i]
		I1 = [p for p in I if G.node[p]['cid']==ids]
		E1 = [(v1,v2) for (v1,v2) in E if v2 in I1]
		#f.write(str(I1)+'\n')
		#f.write(str(E1)+'\n')
		m.addConstr(quicksum(vars[E_dict[(v1,v2)][0],E_dict[(v1,v2)][1]] for (v1,v2) in E if v2 in I1)==1)
		m.addConstr(quicksum(vars[E_dict[(v1,v2)][0],E_dict[(v1,v2)][1]] for (v1,v2) in E if v1 in I1)==1)
	

	m.update
	#f.close()
		
		
	# Optimize model
	m._vars = vars
	m.params.LazyConstraints = 1
	m.optimize(subtourelim)
	solution = m.getAttr('x', vars)
	selected = [(E_dict[e][0],E_dict[e][1]) for e in E if solution[E_dict[e][0],E_dict[e][1]] == 1 and not(G.node[e[0]]['kind']==3 or G.node[e[1]]['kind']==3)]
	assert len(subtour(selected)) ==0
	m.write('./milp/model.sol')
	#print('Obj: %g' % m.objVal)
	return Node_dict, m.objVal
	
	
		







