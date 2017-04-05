#!/bin/bash

# Call the script to set the environment
python config/scripts/setenv.py

# Set PYTHONPATH to point to the codebase
NEW=`python config/scripts/get_env_src.py`
export PYTHONPATH=$PYTHONPATH:$NEW

# Set the PROJECT_ROOT
PROJECT_DIR=`python config/scripts/get_env_dir.py`
echo $PROJECT_DIR
export PROJECT_ROOT=$PROJECT_DIR
