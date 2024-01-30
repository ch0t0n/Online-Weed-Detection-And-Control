import sys
sys.path.insert(0,'./cost')
import edge_cost


def sign(p1, p2, p3):
	"""
	input:
		p1 - apoint
		p2 - a point
		p3 - a point
	output:
		D = -1/1/0 [1 - clockwise, -1 - anticlock wise, 0 - online(no rotation)]
	"""
	D =  0
	d = (p3[0]-p1[0])*(p2[1]-p1[1]) - (p3[1]-p1[1])*(p2[0]-p1[0])
	if d > 0:
		D = 1
	elif d < 0:
		D = -1
	else:
		D = 0
	return D


def get_action(G, path, vl, omega):
	"""

	"""
	action = []
	observation = []
	if len(path)==0:
		return action
	current = path[0]
	observation = [current[1]]
	for i in range(len(path)-1):
		next = path[i+1]
		
		if G.node[current]['kind']==0:
			rot_time = edge_cost.rot_cost(current[0], current[1], next[1], omega)
			D = sign(current[0], current[1], next[1])
			action.append(('R', D, rot_time))
			move_time = edge_cost.dist_cost(current[1], next[1], vl)
			action.append(('M', move_time))
		elif G.node[current]['kind']==1:
			s_time = G.node[current]['cost']
			action.append(('S', s_time))
			rot_time = edge_cost.rot_cost(current[0], current[1], next[1], omega)
			D = sign(current[0], current[1], next[1])
			action.append(('R', D, rot_time))
			move_time = edge_cost.dist_cost(current[1], next[1], vl)
			action.append(('M', move_time))
		elif  G.node[current]['kind']==2:
			f_time = G.node[current]['cost']
			action.append(('F', f_time))
			rot_time = edge_cost.rot_cost(current[0], current[1], next[1], omega)
			D = sign(current[0], current[1], next[1])
			action.append(('R', D, rot_time))
			move_time = edge_cost.dist_cost(current[1], next[1], vl)
			action.append(('M', move_time))
		current = next
	
	s_time = G.node[current]['cost']
	if G.node[current]['kind']==1:
		action.append(('S', s_time))
	return action

def extract_actions(G, paths, vl, omega):
	"""

	"""
	Actions = {}
	for (key, path) in paths.items():
		action = get_action(G, path, vl, omega)
		Actions[key] = action
	return Actions


		
		
		
	

