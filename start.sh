#!/usr/bin/env bash
#The name of the container used during installation
VENV_NAME=app-container

#Activate the container and invoke the gui
source ./app-container/bin/activate
#These variables are set based on their values when the install script is executed. Re-set values as needed.
python -u src/main.py
