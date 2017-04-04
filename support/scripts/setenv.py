'''
Script that sets the environment of the current project
'''

import os
import json

def check_env(env):
	envs_str = os.popen("conda info --envs").read()
	ini_ind = envs_str.find("*")
	end_ind = envs_str[ini_ind:].find("\n")
	sub_str = envs_str[ini_ind:end_ind+ini_ind]
	retr_env = sub_str[-len(env):]
	return retr_env == env

# These scripts are supposed to be called from the root directory of the project
# Load the conda environment configuration and check and install packages
with open(os.path.join('config', 'conda_setup.json'), 'r') as fp:
	conda_setup = json.load(fp)

# Load the environment variables
with open(os.path.join('config', 'project_vars.json'), 'r') as fp:
	VARS = json.load(fp)

# Check the environment
if check_env(VARS['PROJECT_NAME']):
	print ("[OK] Project environment set")
else:
	print ("[ERROR] Set the project environment, run \"source activate " + VARS["PROJECT_NAME"] + "\"")
	exit()

# For all the packages in pip, loop
for packg in conda_setup['pip'].keys():
	if conda_setup['pip'][packg] != "":
		os.system("pip install " + packg + "==" + conda_setup['pip'][packg])
	else:
		os.system("pip install " + packg)
