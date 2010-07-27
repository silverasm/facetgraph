import random
#in-house
from dbsetup import *

thisHost = "http://localhost/~aditi/cgi-bin/dev"
newgraph = "newgraph.py"
currentY = [0,0,0,0]

def getRandPos(level):
	i = 0
	y = currentY[level] + 60
	currentY[level] = y
	return {"x": (level+1)*200, "y":y}

def getTwoLevelData(queries, n):
	data = {}
	for query in queries:
		L1Instances = session.query(WordToWordRI).order_by(WordToWordRI.rank).filter(WordToWordRI.query == query)[:n]
		data[L1Instances[0].query.lower()] = {}
		#print data
		for instance in L1Instances:
			data[instance.query.lower()][(instance.result.lower(), instance.rank)]=[]
		
		for l1 in data.keys():
			for l2 in data[l1].keys():
				L2Instances = session.query(WordToWordRI).order_by(WordToWordRI.rank).filter(WordToWordRI.query==l2[0])[:n]
				for instance in L2Instances:
					data[l1][l2].append((instance.result.lower(), instance.rank))
	
	nodes= []
	edges = []
	nodeIDs = {}
	id = -1;
	for l1 in data.keys():
		id += 1
		name = l1
		if name in nodeIDs:
			L1id = nodeIDs[name]
		else:
			L1id = str(id)
			nodeIDs[name] = L1id
			niceName = name
			# different kinds of urls?
			newGraphURL = "%s/%s?query=%s&n=%s"%(thisHost, newgraph, query, n)
			nodes.append({"id": L1id, "level": 0, "name":name, "components": [{"type":"text", "name":niceName, "url":newGraphURL}], "position":getRandPos(0)})
	for l1 in data.keys():
		L1id = nodeIDs[l1]
		for l2, rank in data[l1]:
			id += 1
			name = l2
			if name in nodeIDs:
				nodeID = nodeIDs[name]
			else:
				nodeID = str(id)
				nodeIDs[name]=nodeID
				niceName = name
				newGraphURL = "%s/%s?query=%s&n=%s"%(thisHost, newgraph, name, n)
				nodes.append({"id": nodeID, "level": 1, "rank":rank, "name":name, "components": [{"type":"text", "name":niceName, "url":newGraphURL}], "position":getRandPos(1)})
			edges.append({"from":L1id, "to": nodeID})
		for l2, rank in data[l1]:
			nodeID = nodeIDs[l2]
			for deepL1, rank in data[l1][(l2, rank)]:
				name = deepL1
				if name in nodeIDs:
					l3ID = nodeIDs[name]
				else:
					id +=1
					l3ID = str(id)
					nodeIDs[name]=l3ID
					niceName = name
					newGraphURL = "%s/%s?query=%s&n=%s"%(thisHost, newgraph, name, n)
					nodes.append({"id": l3ID, "level": 2, "rank":rank, "name":name, "components": [{"type":"text", "name":niceName, "url":newGraphURL}], "position":getRandPos(2)})
				edges.append({"from":nodeID, "to": l3ID})
	return {"nodes":nodes, "edges":edges, "nodeIDs":nodeIDs}
			