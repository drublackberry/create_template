'''
Script that replicates and environment for a python data science project
author: Andreu Mora (andreu.mora@gmail.com)
'''

import os
import getpass
import json

debug = False
var_dict = {}

def raise_error (msg):
	print ("[ERROR]: " + msg)
	exit()

def confirm_var (var, value):
	if debug:
		print ("[DEBUG] Variable = " + var + " set to " + str(value))
	var_dict[var] = value


# Prompt for project variables
print ("Welcome to Wet Gremlin, an utility to create project environments.")
PROJECT_NAME = input("Please enter the project name []: ")
if PROJECT_NAME == "":
	raise_error("The project name cannot be left empty")
confirm_var('PROJECT_NAME', PROJECT_NAME) 

# Prompt for author and email
AUTHOR_NAME = input("Enter author's name: ")
confirm_var('AUTHOR_NAME', AUTHOR_NAME)
AUTHOR_MAIL = input("Enter author's email: ")
confirm_var('AUTHOR_MAIL', AUTHOR_MAIL)
DESCRIPTION = input("Enter the project description: ")
confirm_var('DESCRIPTION', DESCRIPTION)


# Project folder
default_dir = "/home/"+getpass.getuser()+"/Documents/"+PROJECT_NAME
dir_ok = False
while not dir_ok:
	PROJECT_DIR = input ("Project directory ["+default_dir+"]: ")
	if PROJECT_DIR == "":
		PROJECT_DIR = default_dir
	if not os.path.exists(PROJECT_DIR):
		confirm_var('PROJECT_DIR', PROJECT_DIR)
		os.makedirs(PROJECT_DIR)
		dir_ok = True
	else:
		raise_error("Selected directory already exists, choose a different one")

# Create all the folders needed in the selected directory
folder_list = ['notebook', 'output', 'config', 'data', 'test', 'wiki']
foo = [os.makedirs(os.path.join(PROJECT_DIR, x)) for x in folder_list]
subfolder_dict = { 'config':['scripts'], 'data': ['in', 'out', 'tmp']}
for i in subfolder_dict.keys():
	for j in subfolder_dict[i]:
		os.makedirs(os.path.join(PROJECT_DIR, i, j))



# Create a specific conda environment
python_ok = False
default_python_ver = '3.6'
while not python_ok:
	PYTHON_VER = input("Select the Python version (["+default_python_ver+"], 2.7): ")
	if PYTHON_VER == '':
		PYTHON_VER = '3.6'
	if PYTHON_VER == '3.6' or PYTHON_VER == '2.7':
		python_ok = True
		confirm_var ('PYTHON_VER', PYTHON_VER)
		ret_conda = os.system("conda create --name "+PROJECT_NAME+" python="+PYTHON_VER)
		if ret_conda != 0:
			raise_error("Conda environment could not be created, see log for errors")

# Create a pointer in src to the codebase
os.makedirs(os.path.join(PROJECT_DIR, 'src'))
os.system("cp ./support/template/__init__.py "+os.path.join(PROJECT_DIR,'src'))
PYTHONPATH_LIST = [os.path.join(PROJECT_DIR, 'src')]
use_external = input("Use external codebase ([y]/n)?: ")
if use_external=="y" or use_external=="":
	src_ok = False
	while not src_ok:
		new_src_dir = input("Type the directory where the codebase is: ")
		if new_src_dir != "":
			PYTHONPATH_LIST.append(new_src_dir)
			add_more = input ("Add another external codebase? (y/[n])?: ")
			if add_more.lower() == 'y':
				src_ok = False
			else:
				src_ok = True
		else:
			print ("Not valid. External codebase cannot be left empty")
print ("External codebases can be added later on to PYTHONPATH manager in project_vars.json")
confirm_var ('PYTHONPATH_LIST', PYTHONPATH_LIST)

# Copy the scripts and default items
os.system("cp ./support/template/conda_setup.json "+os.path.join(PROJECT_DIR,'config'))
os.system("cp ./support/template/.gitignore "+os.path.join(PROJECT_DIR))
os.system("cp ./support/template/wiki.md "+os.path.join(PROJECT_DIR, 'wiki'))
os.system("cp ./support/scripts/setenv.py "+os.path.join(PROJECT_DIR, 'config', 'scripts'))
os.system("cp ./support/scripts/get_env_name.py "+os.path.join(PROJECT_DIR, 'config', 'scripts'))
os.system("cp ./support/scripts/get_env_src.py "+os.path.join(PROJECT_DIR, 'config', 'scripts'))
os.system("cp ./support/scripts/get_env_dir.py "+os.path.join(PROJECT_DIR, 'config', 'scripts'))
os.system("cp ./support/scripts/get_env_pythonpath.py "+os.path.join(PROJECT_DIR, 'config', 'scripts'))
os.system("cp ./support/scripts/setenv.sh "+PROJECT_DIR)
os.system("cp ./support/scripts/wgutils.py "+os.path.join(PROJECT_DIR, 'src'))


# Create a README file
text_file = open(os.path.join(PROJECT_DIR, "README.md"), "w")
text_file.write("## Project "+PROJECT_NAME+"\n")
text_file.write(DESCRIPTION+"\n\n\n")
text_file.write("Author: "+AUTHOR_NAME+" ("+AUTHOR_MAIL+")\n")
text_file.write("## Dependencies\n")
text_file.write("* Needs python 3 to execute the installation script\n")
text_file.write("* Needs conda to manage virtual environments\n")
text_file.write("* Virtual environment dependencies can be found in config/conda_setup.json\n\n")
text_file.write("Project template created with Wet Gremlin (https://github.com/drublackberry/wet-gremlin)\n")
text_file.close()

# Store the environment variables in a json file
with open(os.path.join(PROJECT_DIR,'config', 'project_vars.json'), 'w') as fp:
	json.dump(var_dict,fp, indent=4, sort_keys=True)

# Configure git
try:
	os.chdir(PROJECT_DIR)
	print(os.getcwd())
	os.system("git init")
	os.system("git add .")
	os.system("git commit -m \"First commit from project creation \"")
	REMOTE_GIT_ADD = input("Add remote git repository? ([y]/n): ")
	if REMOTE_GIT_ADD.lower() == 'y' or REMOTE_GIT_ADD == '':
		REMOTE_GIT = input("Enter remote address: ")
		os.system("git remote add origin "+REMOTE_GIT)
		os.system("git push -u origin master")
except:
	print ("[ERROR] Git not installed or not configured. Try manually.")

