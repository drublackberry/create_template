import os
import json

# Load the environment variables
with open(os.path.join('config', 'project_vars.json'), 'r') as fp:
        VARS = json.load(fp)

print (VARS['PROJECT_NAME'])
