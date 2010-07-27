#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7

#v 2.7 July 17th 2010 Author: Aditi Muralidharan aditi@cs.berkeley.edu
# Loads a new reverted index graph from the database
import os
os.environ['PYTHON_EGG_CACHE'] = '/tmp'

import cgi
import simplejson

form = cgi.FieldStorage()

#in-house
import getdata
#import graphlib

print "Content-type: application/json\n\n"

encoder = simplejson.JSONEncoder()
queryType = "camera"
resultType = "feature"
if "querytype" in form and "resulttype" in form:
	queryType = form["querytype"].value 
	resultType = form["resulttype"].value

queries = None
N1 = 4
if "n1" in form:
	N1 = int(form["n1"].value)
if "n2" in form:
	N2 = int(form["n2"].value)
else:
	N2 = N1

if "query" in form:
	queries = []
	args = form["query"].value.split(",")
	for arg in args:
		if queryType in ["word", "feature"]:
			queries.append(arg.strip())
		elif queryType == "camera" and resultType == "feature":
			queries.append(arg.strip())
		else:
			queries.append(int(arg.strip()))
elif queryType =="word":
	queries=["waterproof"]
elif queryType == "topic":
	queries= [0]
elif queryType =="feature":
	queries = ["zoom"]
elif queryType =="camera" and resultType != "feature":
	queries = [3]
elif queryType =="camera" and resultType == "feature":
	queries = ["canon powershot a570"]
else:
	print encoder.encode({})

data = getdata.getTwoLevelData(queryType, resultType, queries, N1, N2)
print encoder.encode(data)

# 	if data != {}:
# 		graph = graphlib.processTwoLevelData(data)
# 	else:
# 		graph = {}
# 	print encoder.encode(graph)
# 	return

	
	
		
	
	
	




