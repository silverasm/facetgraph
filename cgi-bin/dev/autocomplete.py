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

query = "ca"
if "query" in form:
	query = form["query"].value

suggestions = []

"""
	Query the appropriate class
"""
limit = 40

instances = session.query(WordToWordRI.query).filter(WordToWordRI.query.startswith(query))[:]
for instance in instances:
	if instance[0].lower() not in suggestions:
		suggestions.append(instance[0].lower())
print simplejson.dumps({"query":query, "suggestions":suggestions})