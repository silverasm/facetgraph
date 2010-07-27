import random
#in-house
from dbsetup import *

thisHost = "http://localhost/~aditi/cgi-bin/facetgraph"
newgraph = "newgraph.py"
currentY = [0,0,0,0]

def getRandPos(level):
	i = 0
	y = currentY[level] + 60
	currentY[level] = y
	return {"x": (level+1)*200, "y":y}


def handleRI(queryType, resultType, queries, N1, N2):
	data = {}
	for query in queries:
		if type(query) is type('string'):
			L1Instances = session.query(RI).order_by(RI.rank).filter(RI.queryType == queryType).filter(RI.resultType == resultType).filter(RI.query.startswith(query))[:N1]
		else:
			L1Instances = session.query(RI).order_by(RI.rank).filter(RI.queryType == queryType).filter(RI.resultType == resultType).filter(RI.query==query)[:N1]

		for instance in L1Instances:
			data[instance.query.lower()] = {}
		#print data
		for instance in L1Instances:
			data[instance.query.lower()][(instance.result.lower(), instance.rank)]=[]
		
		for l1 in data.keys():
			for l2 in data[l1].keys():
				if type(l2[0]) is type('string'):
					L2Instances = session.query(RI).order_by(RI.rank).filter(RI.queryType == resultType).filter(RI.resultType == queryType).filter(RI.query.startswith(l2[0]))[:N2]
				else:
					L2Instances = session.query(RI).order_by(RI.rank).filter(RI.queryType == resultType).filter(RI.resultType == queryType).filter(RI.query == l2[0])[:N2]
				for instance in L2Instances:
					data[l1][l2].append((instance.result.lower(), instance.rank))
	
	nodes= []
	edges = []
	nodeIDs = {}
	id = -1;
	for l1 in data.keys():
		id += 1
		if queryType == "camera":
			name = getCameraName(id)
		else:
			name = l1
		if name in nodeIDs:
			L1id = nodeIDs[name]
		else:
			L1id = str(id)
			nodeIDs[name] = L1id
			niceName = name
			# different kinds of urls?
			newGraphURL = "%s/%s?querytype=%s&resulttype=%s&query=%s&n1=%d&n2=%d"%(thisHost, newgraph, queryType, resultType, query, N1, N2)
			nodes.append({"id": L1id, "level": 0, "name":name, "components": [{"type":"text", "name":niceName, "url":newGraphURL}], "position":getRandPos(0)})
	for l1 in data.keys():
		L1id = nodeIDs[l1]
		for l2, rank in data[l1]:
			id += 1
			name = l2
			if resultType == "camera":
				name = getCameraName(l2)
			if name in nodeIDs:
				nodeID = nodeIDs[name]
			else:
				nodeID = str(id)
				nodeIDs[name]=nodeID
				niceName = name
				newGraphURL = "%s/%s?querytype=%s&resulttype=%s&query=%s&n1=%d&n2=%d"%(thisHost, newgraph, resultType, queryType, l2, N1, N2)
				nodes.append({"id": nodeID, "level": 1, "rank":rank, "name":name, "components": [{"type":"text", "name":niceName, "url":newGraphURL}], "position":getRandPos(1)})
			edges.append({"from":L1id, "to": nodeID})
		for l2, rank in data[l1]:
			l2name = l2
			if resultType == "camera":
				l2name = getCameraName(l2)
			nodeID = nodeIDs[l2name]
			for deepL1, rank in data[l1][(l2, rank)]:
				name = deepL1
				if queryType == "camera":
					name = getCameraName(leepL1)
				if name in nodeIDs:
					l3ID = nodeIDs[name]
				else:
					id +=1
					l3ID = str(id)
					nodeIDs[name]=l3ID
					niceName = name
					newGraphURL = "%s/%s?querytype=%s&resulttype=%s&query=%s&n1=%d&n2=%d"%(thisHost, newgraph, queryType, resultType, deepL1, N1, N2)
					nodes.append({"id": l3ID, "level": 2, "rank":rank, "name":name, "components": [{"type":"text", "name":niceName, "url":newGraphURL}], "position":getRandPos(2)})
				edges.append({"from":nodeID, "to": l3ID})
	return {"nodes":nodes, "edges":edges, "nodeIDs":nodeIDs}	


def getTwoLevelData(queryType, resultType, queries, N1, N2):
	if queryType in ["word", "topic", "camera"] and resultType in ["word", "topic", "camera"]:
		return handleRI(queryType, resultType, queries, N1, N2)
	else:
		"""
		"""
		data = {}
		for query in queries:
			RIClass = None
			if queryType == "camera":
				L1Class = cfRevertedIndex
				L1Name = getCameraName
				getL1ID = getCameraID
			elif queryType == "feature" :
				L1Class = fcRevertedIndex
				L1Name = getFeatureName
				getL1ID = getFeatureID
			else:
				return {}
				
			queryID = getL1ID(query)
			# get the top N1 Level 1 rankings for the query.
			L1Instances = session.query(L1Class).order_by(L1Class.rank).filter(L1Class.query == queryID)[:N1]
			data[L1Instances[0].query] ={}
			for instance in L1Instances:
				data[instance.query][(instance.result, instance.rank)] =[]
			
			if resultType == "camera":
				L2Class = cfRevertedIndex
				L2Name = getCameraName
				getL2ID = getCameraID
			elif resultType == "feature" :
				L2Class = fcRevertedIndex
				L2Name = getFeatureName
				getL2ID = getFeatureID
			else:
				return {}
			
			for l1 in data.keys():
				for l2 in data[l1].keys():
					l2ID = l2[0]
					L2Instances = session.query(L2Class).order_by(L2Class.rank).filter(L2Class.query == l2ID)[:N2]
					for instance in L2Instances:
						data[l1][l2].append((instance.result, instance.rank))
			nodes= []
			edges = []
			nodeIDs = {}
			id = -1;
			for l1 in data.keys():
				id += 1
				name = L1Name(l1)
				if name in nodeIDs:
					L1id = nodeIDs[name]
				else:
					L1id = str(id)
					nodeIDs[name] = L1id
					niceName = name.title().replace(" ", "\n")
					# different kinds of urls?
					newGraphURL = "%s/%s?querytype=%s&resulttype=%s&query=%s&n1=%s&n2=%s"%(thisHost, newgraph, queryType, resultType, query, N1, N2)
					nodes.append({"id": L1id, "level": 0, "name":name, "components": [{"type":"text", "name":niceName, "url":newGraphURL}], "position":getRandPos(0)})
				for l2, rank in data[l1]:
					id += 1
					name = L2Name(l2)
					if name in nodeIDs:
						nodeID = nodeIDs[name]
					else:
						nodeID = str(id)
						nodeIDs[name]=nodeID
						niceName = name.title().replace(" ", "\n")
						newGraphURL = "%s/%s?querytype=%s&resulttype=%s&query=%s&n1=%s&n2=%s"%(thisHost, newgraph,resultType, queryType, name, N1, N2)
						nodes.append({"id": nodeID, "level": 1, "rank":rank, "name":name, "components": [{"type":"text", "name":niceName, "url":newGraphURL}], "position":getRandPos(1)})
					edges.append({"from":L1id, "to": nodeID})
					for deepL1, rank in data[l1][(l2, rank)]:
						name = L1Name(deepL1)
						if name in nodeIDs:
							l3ID = nodeIDs[name]
						else:
							id +=1
							l3ID = str(id)
							nodeIDs[name]=l3ID
							niceName = name.title().replace(" ", "\n")
							newGraphURL = "%s/%s?querytype=%s&resulttype=%s&query=%s&n1=%s&n2=%s"%(thisHost, newgraph,queryType, resultType, name, N1, N2)
							nodes.append({"id": l3ID, "level": 2, "rank":rank, "name":name, "components": [{"type":"text", "name":niceName, "url":newGraphURL}], "position":getRandPos(2)})
						edges.append({"from":nodeID, "to": l3ID})
			return {"nodes":nodes, "edges":edges, "nodeIDs":nodeIDs}
