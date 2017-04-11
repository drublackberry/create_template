# Wet Gremlin
Wet Gremlin is an utility to create template project environments easily.

It will automatically do the following things for you:

* Setup the folder structure
* Create a conda virtual environment with all the tools that you need
* Initialize a git repository and link to a remote one
* Manage the external source repositories you might want to call from your code

## Dependencies
Wet Gremlin depends on the following preinstalled packages:

* Python 3
* Conda

## Usage
### Start a new project
To clone a template and start a new project just type
`python create_project.py`
The installer will guide you through the install process.

### Use a project
To start using a project, move to the project directory and type
`source activate PROJECT_NAME`
That will activate the conda environment. Then type
`source setenv.sh`
That will create the necessary environment variables

### Modify a project
The project can be modified. Go to the project directory and navigate to config. There you will find two json objects:

* conda_setup.json contains a dictionary of the packages and version to install and use.
* project_vars.json contains the project variables. To add new variables to the PYTHONPATH use the variable PYTHONPATH_LIST there.


