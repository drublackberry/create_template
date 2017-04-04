#!/bin/bash

# Call the script to set the environment
python config/setenv.py

# Set PYTHONPATH to point to the codebase
NEW=`python config/get_env_src.py`
export PYTHONPATH=$PYTHONPATH:$NEW

