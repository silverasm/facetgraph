#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7

#v 2.7 July 17th 2010 Author: Aditi Muralidharan aditi@cs.berkeley.edu
# Loads a new reverted index graph from the database
import os
os.environ['PYTHON_EGG_CACHE'] = '/tmp'

import cgi
import simplejson

encoder = simplejson.JSONEncoder()
form = cgi.FieldStorage()

#in-house
import getdata
#import graphlib

print "Content-type: application/json\n\n"

queries = ["camera","value"]
n = 6
if "query" in form:
	queries = []
	args = form["query"].value.split(",")
	for arg in args:
		queries.append(arg.strip())

if "n" in form:
	n = int(form["n"].value)

data = getdata.getTwoLevelData(queries, n)
print encoder.encode(data)