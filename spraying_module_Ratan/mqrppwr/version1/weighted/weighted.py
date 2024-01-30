import networkx as nx
import sys
sys.path.insert(0,'./cost')
import edge_cost

#################################
# Start: creation of all nodes
#################################
def nodes_for_drones(G, N, Q, D, C):
	"""
	input:
		G - a directed graph
		N - a number
		Q - list of positions of drones
		D - dictionary for direction of drones
		C - maximum pesticide amount that a drone can carry
	Output:
		G - update G with nodes related to drones
	"""
	#create nodes for drones (qd,q,C)
	for q in Q:
		n = N*q[0]+q[1]
		G.add_node((D[q],q,C), cost=0.0, cid=n, kind=0)
	return G

def nodes_for_plants(G, N, I, Q, T, W, C, vs):
	"""
	input:
		G - a directed graph
		N - a number
		I - list of positions of plants
		Q - list of positions of drones
		T - list of positions of tanks
		W - dictionary for amount of infection to plants
		C - maximum pesticide amount that a drone can carry
		vs - spraying speed
	
	output:
		G - update G with nodes related to plants
	"""

	#create nodes for all plants
	for p in I:
		n = N*p[0] + p[1]
		c  = W[p]/vs
		#create nodes from quadrotor to the plant p
		for q in Q:			
			G.add_node((q,p,C-W[p]), cost =c, cid=n, kind=1)

		#create node for a plant to the plant p
		for q in I:
			if p != q:
				for i in range((C-W[p])+1):
					G.add_node((q,p,i), cost =c, cid=n, kind=1)

		#create node for a tank to the plant p
		for q in T:
			for i in range((C-W[p])+1):
				G.add_node((q,p,i), cost =c, cid=n, kind=1)
	return G


def nodes_for_tanks(G, N, I, T, W, C, vf):
	"""
	input:
		G - a directed graph
		N - a number
		I - list of positions of plants
		T - list of positions of tanks
		W - dictionary for amount of infection to plants
		C - maximum pesticide amount that a drone can carry
		vf - refuelling speed
	output:
		G - update G with nodes related to tank
	"""
	#create nodes for all tanks
	for t in T:
		n = N*t[0]+t[1]

		#create node from a plant to the tank t
		for p in I:
			for i in range(W[p], C+1, 1):
				c = i/vf
				G.add_node((p, t, i), cost =c, cid=n, kind=2)
	return G	



def create_nodes(G, N, I, Q, T, D, W, C, vs, vf):
	"""
	input:
		G - directed graph	
		N - a number used for defining uquique number
		scenario S = (I, Q, T, D, W, C)
		vs - spraying speed
		vf - refuelling speed
	output:
		G - update G with all nodes
		
	"""
	#create nodes for drones
	G = nodes_for_drones(G, N, Q, D, C)
	
	#create nodes for plants
	G = nodes_for_plants(G, N, I, Q, T, W, C, vs)
	
	# create nodes from tanks
	G = nodes_for_tanks(G, N, I, T, W, C, vf)
	
	return G

#################################
# End: creation of all nodes
#################################


#################################
# start: creation of all edges
#################################		
	
def edges_drone_to_plant(G, W, omega, vl):
	"""
	input:
		G - a directed graph
		W - dictionary of infection for plant's position
		omega - angular speed
		vl - linear speed
	output:
		G - update G with edges between drone nodes to plant nodes
	"""
	drone_nodes = [q for q in G.nodes() if G.node[q]['kind']==0]
	plant_nodes = [p for p in G.nodes() if G.node[p]['kind']==1] 
	for q in drone_nodes:
		for p in plant_nodes:
			if (q[1]==p[0]) and (q[0] != p[1]) and (p[2] == q[2] - W[p[1]]):
				ce = edge_cost.edge_cost(q[0], q[1], p[1], omega, vl)
				G.add_edge(q, p, cost =ce)

	return G

def edges_plant_to_plant(G, W, omega, vl):
	"""
	input:
		G - a directed graph
		W - dictionary of infection for plant's position
		omega - angular speed
		vl - linear speed
	output:
		G - update G with edges between plant nodes to plant nodes
	"""
	plant_nodes = [p for p in G.nodes() if G.node[p]['kind']==1] 
	for p1 in plant_nodes:
		for p2 in plant_nodes:
			if (p1[1]==p2[0]) and (p1[0] != p2[1]) and (p2[2] == p1[2] - W[p2[1]]):
				ce = edge_cost.edge_cost(p1[0], p1[1], p2[1], omega, vl)
				G.add_edge(p1, p2, cost =ce)

	return G

def edges_plant_to_tank(G, W, omega, vl, C):
	"""
	input:
		G - a directed graph
		W - dictionary of infection for plant's position
		omega - angular speed
		vl - linear speed
		C - maximum capacity of pesticide that it can carry
	output:
		G - update G with possible edges
	"""
	plant_nodes = [p for p in G.nodes() if G.node[p]['kind']==1]
	tank_nodes = [t for t in G.nodes() if G.node[t]['kind']==2] 
	for p in plant_nodes:
		for t in tank_nodes:
			if (p[1]==t[0]) and (p[0] != t[1]) and (t[2] == C -p[2]):
				ce = edge_cost.edge_cost(p[0], p[1], t[1], omega, vl)
				G.add_edge(p, t, cost =ce)

	return G


def edges_tank_to_plant(G, W, omega, vl, C):
	"""
	input:
		G - a directed graph
		W - dictionary of infection for plant's position
		omega - angular speed
		vl - linear speed
		C - maximum capacity of pesticide that it can carry
	output:
		G - update G with possible edges
	"""
	tank_nodes = [t for t in G.nodes() if G.node[t]['kind']==2]
	plant_nodes = [p for p in G.nodes() if G.node[p]['kind']==1] 
	for t in tank_nodes:
		for p in plant_nodes:
			if (t[1]==p[0]) and (t[0] != p[1]) and (p[2] == C -W[p[1]]):
				ce = edge_cost.edge_cost(t[0], t[1], p[1], omega, vl)
				G.add_edge(t, p, cost =ce)

	return G



	


def create_edges(G, W, omega, vl, C):
	"""
	input:
		G - a directed graph
		W - dictionary of infection for plant's position
		omega - angular speed
		vl - linear speed
	output:
		G - update G with possible edges
	"""
	#create edges between drone nodes to plant nodes
	G = edges_drone_to_plant(G, W, omega, vl)
	#create edges between plant nodes to plant nodes
	G = edges_plant_to_plant(G, W, omega, vl)
	#create edges between plant nodes to tank nodes
	G = edges_plant_to_tank(G, W, omega, vl, C)
	#create edges between tank nodes to plant nodes
	G = edges_tank_to_plant(G, W, omega, vl, C)

	return G

	
				
			


		
			
		
	


def weighted_graph(S, vl, omega, vs, vf, N):
	"""
	input: S = (I, Q, T, D, W, C) scenario
	output:
		G - weighted graph with
	 	node properties
			cost - cost of node 
			cid - cid for each node
			kind - 0 - drone, 1 - plant, 2 - tank
		edge properties
			cost - rotational cost + cost of travel on the edge
	"""
	
	I, Q, T, D, W, C = S[0], S[1], S[2], S[3], S[4], S[5]
	
	#create a graph
	G = nx.DiGraph()
	#create all nodes
	G = create_nodes(G, N, I, Q, T, D, W, C, vs, vf)
	#create edges
	G = create_edges(G, W, omega, vl, C)
	return G
