from sklearn.cluster import KMeans



def get_clstr(cluster_num, X, l):
	Y = []
	for i in range(len(l)):
		if l[i]==cluster_num:
			Y.append(X[i])
	return Y

def clstr_scenario(S):
	'''
	input: S - scenario
	output:LS - cluster of scenario
	'''
	#print(S)
	X= S[0]
	num_of_cluster = len(S[1]) 
	kmeans = KMeans(n_clusters=num_of_cluster)
	kmeans.fit(X)
	l = kmeans.labels_
	#list of each cluster
	Z= []
	for i in range(num_of_cluster):
		Z.append(get_clstr(i, X, l))

	# find center of each cluster
	center = []
	for i in range(num_of_cluster):
		x_mean = float(sum([x[0] for x in Z[i]]))/float(len(Z[i]))
		y_mean = float(sum([x[1] for x in Z[i]]))/float(len(Z[i]))	
		if (x_mean, y_mean) in Z:
			x_mean = x_mean + 0.5
			
		
		center.append((x_mean, y_mean))	
	#list of scenarios
	LS = []
	for i in range(num_of_cluster):
		D = {}
		print(list(S[3].values())[i])
		D[center[i]] = (center[i][0]-0.5, center[i][1])
		W = {}
		for point in Z[i]:
			W[point] = S[4][point]
		

		LS.append((Z[i],[center[i]], S[2], D, W, S[5]))

	return LS
