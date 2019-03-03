@echo off
REM Edit the following variables according to python installation
set PYTHONARCH=64

REM ask user for version of python
REM set /P version64="Is your python installation Python 2.7.* 64-bit? (Y/N): "
REM IF NOT "%version64%"=="Y" IF NOT "%version64%"=="y" (
REM set PYTHONARCH=32
REM echo *************************************************************************************************
REM echo Sorry, this version of Python is currently not supported. Please install Python 2.7 64-bit.
REM echo *************************************************************************************************
REM pause
REM exit
REM )

REM set directory to place Gtk files
set PYTHONPACKAGES_PATH=Lib\site-packages\

REM name the container that will be created
set VENV_NAME=app-container

REM install and start the venv container
pip install virtualenv
virtualenv "%VENV_NAME%"

IF %PYTHONARCH%==64 (
echo Processing using a 64-bit python27 installation
%VENV_NAME%\Scripts\activate & pip install lxml & pip install configparser & xcopy python27-64bit-gtk3\* "%VENV_NAME%" /E /Y & %VENV_NAME%\Scripts\deactivate
REM Now create the file that will start the gui
echo REM the name of the container used during installation > start.bat
echo set VENV_NAME=app-container >> start.bat
echo. >> start.bat
echo REM activate the container and invoke the gui >> start.bat
echo %VENV_NAME%\Scripts\activate ^& pythonw -u src/main.pyw ^& deactivate >> start.bat
echo Type: start.bat to start the application
)

