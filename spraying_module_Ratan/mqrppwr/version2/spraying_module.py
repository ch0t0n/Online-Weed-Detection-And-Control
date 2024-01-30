
def spraying_path(weed_map):    
    import time
    import sys
    spraying_path = 'Codes/spraying_module_Ratan/mqrppwr/version2'
    sys.path.append(spraying_path+'/scenario')
    import scenario
    sys.path.append(spraying_path+'/weighted')
    sys.path.append(spraying_path+'/cost')
    import weighted
    sys.path.append(spraying_path+'/dummy')
    import dummy
    sys.path.append(spraying_path+'/milp')
    import milp
    import objective
    sys.path.append(spraying_path+'/display')
    import display
    sys.path.append(spraying_path+'/paths')
    import path
    import action
    sys.path.append(spraying_path+'/cluster')
    import cluster

    tstime = time.time()
    #Parameters
    vl = 1
    omega = 1
    vs = 1
    vf = 1
    # larger than any coordinate points
    N = 7
    # a number for creating dummy node
    k = N

    # pwd = os.getcwd()
    # config_path = os.path.join(pwd, 'configuration', 'set-1', '1.ini')
    # print(config_path)
    config_path = weed_map

    # read the scenario from the config file
    Sc = scenario.scenario_reader(config_path)

    LS = []
    #when we use clustering
    stime = time.time()
    LS, center, Dall = cluster.clstr_scenario(Sc)
    etime = time.time()
    clTime = etime-stime

    #when we do not use clustring
    LS = []
    LS.append((Sc[0], center, Sc[2], Dall, Sc[4], Sc[5]))
    #print(LS)

    milpTime = 0
    GTime = 0
    OptSol = 0.0
    CmilpTime = 0
    CGTime = 0
    COptSol = 0
    quad =[]
    paths = []
    actions_times = []
    for i in range(len(LS)):	
        S = LS[i]
        stime = time.time()
        #Construct weighted graph from the scenario
        G = weighted.weighted_graph(S, vl, omega, vs, vf, N)
        #Add dummy node
        C = S[5]
        G, dummynode = dummy.add_dummy(G,k,C) 
        etime = time.time()
        CGTime = max(CGTime, etime-stime)
        GTime += etime - stime
        
        #optimization
        stime = time.time()
        Node_dict = milp.optimization(G, dummynode)
        val = objective.getObjective()
        OptSol += val
        etime = time.time()
        CmilpTime = max(CmilpTime, etime-stime)
        milpTime += etime - stime
        
        #path extraction
        paths = path.extract_paths(G, Node_dict)
        # extract actions for each drone
        Actions = action.extract_actions(G, paths, vl, omega)
        print(paths)
        print(Actions)
    tetime = time.time()
    totalTime = tetime - tstime
    print("Total Time for clustering = ", clTime)
    print("Total Time for construction graph = ", GTime)
    print("Total Time for MILP encoding and solving = ", milpTime)
    print("Total cost =", OptSol)
    print("Maximum cluster graph time = ", CGTime)
    print("Maximum cluster miLP time = ", CmilpTime)
    print("Total time = ", totalTime)

    return Sc, paths, Actions, totalTime


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

