#!/usr/bin/env python 

#v 2.7 July 17th 2010 Author: Aditi Muralidharan aditi@cs.berkeley.edu
# Loads a new reverted index graph from the database

import cgi
form = cgi.FieldStorage()
import simplejson

#in-house
import getdata
#import graphlib

print "Content-type: application/json\n\n"

encoder = simplejson.JSONEncoder()
#if "querytype" not in form or "resulttype" not in form:
if True:
	print encoder.encode({})
else:
	#queryType = form["querytype"] 
	#resultType = form["resulttype"]
	queryType = "camera"
	resultType = "feature"
	query = None
	N1 = 4
	N2 = 4
	if "n1" in form:
		N1 = int(form["n1"])
	if "n2" in form:
		N2 = int(form["n2"])
	if "query" in form:
		query = form["query"]
	elif queryType =="camera":
		query="nikon d80"
	elif queryType == "feature":
		query= "camera"
	else:
		print encoder.encode({})
	data = getdata.getTwoLevelData(queryType, resultType, query, N1, N2)
 	print encoder.encode(data)
# 	if data != {}:
# 		graph = graphlib.processTwoLevelData(data)
# 	else:
# 		graph = {}
# 	print encoder.encode(graph)
# 	return

	
	
		
	
	
	




