

def edges_dummy_to_drones(G, dummy):
	"""
	input:
		G - directed graph
		dummy - dummy node
	output:
		G - update G
	"""
	drone_nodes = [q for q in G.nodes() if G._node[q]['kind']==0]
	for q in drone_nodes:
		G.add_edge(dummy, q, cost=0.0)
	return G

def edges_drones_to_dummy(G, dummy):
	"""
	input:
		G - directed graph
		dummy - dummy node
	output:
		G - update G
	"""
	drone_nodes = [q for q in G.nodes() if G._node[q]['kind']==0]
	for q in drone_nodes:
		G.add_edge(q, dummy, cost=0.0)
	return G




def edges_plants_to_dummy(G, dummy):
	"""
	input:
		G - directed graph
		dummy - dummy node
	output:
		G - update G
	"""
	plant_nodes = [p for p in G.nodes() if G._node[p]['kind']==1]
	for p in plant_nodes:
		G.add_edge(p, dummy, cost=0.0)
	return G

def add_dummy(G, k, C):
	"""
	input: G - a directed graph
	output: G - update G with dummy vertex
	"""
	dummy = ((k,k), (k,k), C)
	G.add_node(dummy, cost =0, cid=0, kind=3)
	G = edges_dummy_to_drones(G, dummy)
	G = edges_plants_to_dummy(G, dummy)
	G = edges_drones_to_dummy(G, dummy)
	return G, dummy


	
