#!/usr/bin/env bash

#environment variables have default values, but should be set before calling the installer
if [ -z "$VENV_NAME" ]; then
    echo "Warning: VENV_NAME was not set, using: app-container" 
    VENV_NAME=app-container
fi

python2 -m pip install virtualenv
virtualenv $VENV_NAME

source ./$VENV_NAME/bin/activate
#creator dependencies
apt-get install python-gi
apt-get install python-pip
apt-get install libgirepository1.0-dev
apt-get install libdbus-1-dev
apt-get install python-dbus

pip install virtualenv
virtualenv $VENV_NAME

source ./$VENV_NAME/bin/activate
#creator dependencies
pip install pygobject
pip install vext
pip install vext.gi
pip install configparser

#Generate the script 
echo "#!/usr/bin/env bash" > start.sh
echo "#The name of the container used during installation" >> start.sh
echo VENV_NAME=$VENV_NAME >> start.sh
echo >> start.sh
echo "#Activate the container and invoke the gui" >> start.sh
echo source ./$VENV_NAME/bin/activate >> start.sh
echo "#These variables are set based on their values when the install script is executed. Re-set values as needed." >> start.sh
echo python -u src/main.py >> start.sh

chmod 755 start.sh
echo
echo
echo Type: ./start.sh to start the application

