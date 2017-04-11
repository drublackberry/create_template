import os
import json

# Load the environment variables
with open(os.path.join('config', 'project_vars.json'), 'r') as fp:
        VARS = json.load(fp)
out_str = ''
for i in VARS['PYTHONPATH_LIST']:
	out_str = out_str + ":"+i
print (out_str)

