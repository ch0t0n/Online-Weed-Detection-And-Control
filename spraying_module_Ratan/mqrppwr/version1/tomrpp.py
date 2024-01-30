import sys
import os
import time

sys.path.insert(0,'./scenario')
import scenario

sys.path.insert(0,'./weighted')
import weighted

sys.path.insert(0,'./dummy')
import dummy

sys.path.insert(0,'./milp')
import milp

sys.path.insert(0,'./display')
import display

sys.path.insert(0,'./paths')
import path 
import action

sys.path.insert(0, './cluster')
import cluster

start = time.time()
s_total = time.time()
#Parameters
vl = 1
omega = 1
vs = 1
vf = 1
# larger than any coordinate points
N = 7
# a number for creating dummy node
k = N

# read the scenario from the config file
Sc = scenario.scenario_reader(sys.argv[1])
LS = []

#when we use clustering
#LS = cluster.clstr_scenario(Sc)
#when we do not use clustring
LS.append(Sc)
#print(LS)
end = time.time()
init_time = end-start
#max time for graph construction
Tg_max = 0.0
#max optimal time
T_opt = 0.0
# additional
T_others = 0.0
#total time
T_total = init_time
#max time
T_max = 0.0

# cost 
J = 0.0
for i in range(len(LS)):
	Tg_start = time.time()
	S = LS[i]
	#print(S)
	#Construct weighted graph from the scenario
	G = weighted.weighted_graph(S, vl, omega, vs, vf, N)

	#Add dummy node
	C = S[5]
	G, dummynode = dummy.add_dummy(G,k,C) 
	Tg_end = time.time()
	if (Tg_end-Tg_start) > Tg_max:
		Tg_max = Tg_end-Tg_start
	
	Opt_start = time.time()
	#optimization
	#print("MILP")
	Node_dict, objval = milp.optimization(G, dummynode)
	J += objval
	#print("MILP")
	Opt_end = time.time()
	if (Opt_end-Opt_start) > T_opt:
		T_opt = Opt_end-Opt_start
	
	#path extraction
	other_start = time.time()
	paths = path.extract_paths(G, Node_dict)
	print(paths)
	# extract actions for each drone
	Actions = action.extract_actions(G, paths, vl, omega)
	print(Actions)
	other_end = time.time()
	if (other_end-other_start) > T_others:
		T_others = other_end-other_start
	#print(paths)
	#print(Actions)
	if init_time + Tg_max + T_opt +T_others > T_max:
		T_max = init_time + Tg_max + T_opt +T_others 

	T_total += (Tg_end-Tg_start) + (Opt_end-Opt_start) + (other_end-other_start)

print("Total cost = ", J)
print("Max Time for construction graph = ", Tg_max)
print("Max Time for MILP encoding and solving = ", T_opt)
print("Max Time for extraction = ", T_others)
print("Maximum Total time = ", T_max)
print("Total time = ", T_total)


#display graph
#display.display_graph(G)



'''
Gd = dm.intro_dummy_vertex(eG, C, max_r_c)
opt.milp(eGd)
os.system('gcc -Wall lp.c -lglpk -o lp')
os.system('./lp > ./direction/solution.txt')
paths = dr.get_paths(max_r_c, C)
print(paths)
'''

