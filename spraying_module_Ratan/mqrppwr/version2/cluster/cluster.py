from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import random


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
	fig = plt.figure()
	ax1 = fig.add_subplot(111)
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
			x_mean = x_mean - 0.5
			
		
		center.append((x_mean, y_mean))	
	#list of scenarios
	LS = []
	Dall = {}
	Wall = {}

	#colors
	number_of_colors = num_of_cluster
	color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_colors)]
	for i in range(num_of_cluster):
		D = {}
		D[center[i]] = (center[i][0]+0.5, center[i][1]+0.5)
		Dall[center[i]] = (center[i][0]+0.5, center[i][1]+0.5)
		W = {}
		for point in Z[i]:
			W[point] = S[4][point]
			Wall[point] = S[4][point]
		x = [p[0] for p in Z[i]]
		y = [p[1] for p in Z[i]]
		
		ax1.scatter(x, y, s=10, c=color[i], marker="s")
		if len(x)==1:
			ax1.scatter([center[i][0]-1], [center[i][1]-1], c=color[i], marker='x')
		else:
			ax1.scatter([center[i][0]], [center[i][1]], c=color[i], marker='x')
		
		LS.append((Z[i],[center[i]], S[2], D, W, S[5]))

	#plt.legend(loc='upper left');
	plt.show(block=False)

	return LS, center, Dall
