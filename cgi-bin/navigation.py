#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7
#v 2.7 July 17th 2010 Author: Aditi Muralidharan aditi@cs.berkeley.edu

"""
This file parametrizes the "top search bar". Include any fields
that are relevant to the new graph. 

Each field must have the following information:

name: the name of the parameter submitted to the cgi-script
type: the kind of input
parameters: the parameters of the input, eg. placeholder text, range, option
values

In addition, the action field must specify a cgi script responsible for 
creating a new graph. (default: newgraph.py)

"""
import simplejson
print "Content-type: application/json\n\n"


topbar = {"action": "newgraph.py"}
inputs = []

inputs.append({"name":"querytype", 
				"label": "Start with the",
               "type":"select", 
               "parameters":{"options":[{"value":"camera", "text":"Cameras"},
                                        {"value":"feature", "text":"Features", "selected":"selected"}
                                        ]
                             }
               })
               
inputs.append({"name":"query", 
			   "label": "called",
               "type":"text", 
               "parameters":{ "value":"zoom"
                             }
               })

inputs.append({"name":"resulttype", 
               "type":"select",
               "label": "and show highly ranked",
               "parameters":{"options":[{"value":"camera", "text":"Cameras"},
                                        {"value":"feature", "text":"Features"}
                                        ]
                             }
               })

inputs.append({"name":"n1",
               "type":"number",
               "label":"Number of results",
               "parameters":{"min":1,
                             "max":10,
                             "step":1,
                             "value":4
                             }})

inputs.append({"name":"", "type":"submit", "parameters":{"value":"Go"}})

topbar["inputs"] = inputs

print simplejson.dumps(topbar)

