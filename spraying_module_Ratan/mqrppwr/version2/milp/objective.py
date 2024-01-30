
def getObjective():
	f = open('./Codes/spraying_module_Ratan/mqrppwr/version2/milp/model.sol', 'r')
	contents = f.readlines()
	val = float(contents[0].split(' = ')[1].strip('\n'))
	print(val)
	f.close()
	return val

#getObjective()
	
