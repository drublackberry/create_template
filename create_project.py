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
print ("Project template utility")
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
folder_list = ['figures', 'notebook', 'output', 'config', 'data', 'test', 'wiki']
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
src_ok = False
while not src_ok:
	create_src = input("Create a link to external codebase ([y]/n)?: ")
	if create_src == "y" or create_src=="":
		SRC_DIR = input("Type the directory where the codebase is: ")
		if SRC_DIR != "":
			os.system("ln -s "+SRC_DIR + " " + os.path.join(PROJECT_DIR, 'src'))
			confirm_var ('SRC_DIR', SRC_DIR)
			src_ok = True
	else:
		os.makedirs(os.path.join(PROJECT_DIR, 'src'))
		confirm_var ('SRC_DIR', os.path.join(PROJECT_DIR, 'src'))
		src_ok = True

# Copy the scripts and default items
os.system("cp ./support/template/conda_setup.json "+os.path.join(PROJECT_DIR,'config'))
os.system("cp ./support/template/.gitignore "+os.path.join(PROJECT_DIR))
os.system("cp ./support/scripts/setenv.py "+os.path.join(PROJECT_DIR, 'config', 'scripts'))
os.system("cp ./support/scripts/get_env_name.py "+os.path.join(PROJECT_DIR, 'config', 'scripts'))
os.system("cp ./support/scripts/get_env_src.py "+os.path.join(PROJECT_DIR, 'config', 'scripts'))
os.system("cp ./support/scripts/setenv.sh "+PROJECT_DIR)

# TODO: Git init the project and link to remote directory


# Create a README file
text_file = open(os.path.join(PROJECT_DIR, "README.md"), "w")
text_file.write("## Project "+PROJECT_NAME+"\n")
text_file.write(DESCRIPTION+"\n")
text_file.write("Author: "+AUTHOR_NAME+" ("+AUTHOR_MAIL+")\n")
text_file.write("## Dependencies\n")
text_file.write("* Needs python 3 to execute the installation script\n")
text_file.write("* Needs conda to manage virtual environments\n")
text_file.write("* Virtual environment dependencies can be found in config/conda_setup.json\n")
text_file.close()

# Store the environment variables in a json file
with open(os.path.join(PROJECT_DIR,'config', 'project_vars.json'), 'w') as fp:
	json.dump(var_dict,fp, indent=4, sort_keys=True)



