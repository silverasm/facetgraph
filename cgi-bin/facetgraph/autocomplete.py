#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7

"""
	OPTIONAL. For use with the JQuery autocomplete library
	downloadable at http://www.devbridge.com/projects/autocomplete/

	Utilities for autocompleting query names using the database
"""
import os
os.environ['PYTHON_EGG_CACHE'] = '/tmp' # a directory to which apache can write
import cgi
import simplejson
#in-house
from dbsetup import * # database information and API classes

print "Content-type: application/json\n\n"

form = cgi.FieldStorage()

query = "c"
if "query" in form:
	query = form["query"].value

type = "camera"
if "type" in form:
	type = form["type"].value

suggestions = []

"""
	Query the appropriate class
"""
limit = 40

if type == "feature":
	instances = session.query(ShortFeature).filter(ShortFeature.shortFeature.startswith(query) )[:limit]
	for instance in instances:
		suggestions.append(instance.shortFeature)
elif type == "camera":
	instances = session.query(Camera).filter(Camera.make.startswith(query))[:limit]
	instances.extend(session.query(Camera).filter(Camera.model.startswith(query))[:limit])
	for instance in instances:
		suggestions.append("%s %s"%(instance.make, instance.model))
	
elif type in [ "word", "topic", "camera"]:
	instances = session.query(RI.query).filter(RI.query.startswith(query)).filter(RI.queryType == type)[:]
	for instance in instances:
		if instance[0] not in suggestions:
			suggestions.append(instance[0])
		
print simplejson.dumps({"query":query, "suggestions":suggestions[:limit]})