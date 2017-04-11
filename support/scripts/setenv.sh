#!/bin/bash

# Call the script to set the environment
python config/scripts/setenv.py

# Set PYTHONPATH to point to the codebase
NEW_PYTHONPATH=`python config/scripts/get_env_pythonpath.py`
export PYTHONPATH=$PYTHONPATH:$NEW_PYTHONPATH

# Set the PROJECT_ROOT
PROJECT_DIR=`python config/scripts/get_env_dir.py`
export PROJECT_ROOT=$PROJECT_DIR
