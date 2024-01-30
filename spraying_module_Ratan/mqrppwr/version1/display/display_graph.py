import networkx as nx
import matplotlib.pyplot as plt

def vertex_color(G, pos, V, color):
	"""
	input: G - graph
		V - a subset of vertices
		shape - shape of vertex
		color - color of all vertices in V
	output:
		G - updated graph
	"""
	
	nx.draw_networkx_nodes(G,pos,nodelist=V,node_color=color)		

	return G

def edge_color(G, pos, E, color):
	"""
	input: G - graph
		E - a subset of vertices
		color - color of all edges in E
	output:
		G - updated graph
	"""
	nx.draw_networkx_edges(G,pos,edgelist=E,edge_color=color)		
	return G

def display_graph(G):
	"""
	input: G -  graph
	output: save the display of graph in file graph.png
	"""
	v1 = G.nodes()[0]
	v2 = G.nodes()[1]
	v3 = G.nodes()[2]
	
	G.add_edge(v1,v2)
	G.add_edge(v2,v3)
	
	#pos=nx.spring_layout(G) 
	#pos=nx.shell_layout(G) 
	pos = nx.circular_layout(G)
		
	V = G.nodes()
	G = vertex_color(G, pos, V, 'green')
	E = G.edges()
	G = edge_color(G,pos, E,'red')
	
	edge_labels=dict([((u,v,),d['cost'])
             for u,v,d in G.edges(data=True)])
	nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
	plt.show()


