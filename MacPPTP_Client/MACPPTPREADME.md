# Mac PPTP App

The Mac PPTP app is a python and ui script that utilizes sudo terminal commands to open a pptp connection to the server. 

## Installation

First need to install PyQt5

```bash
pip install PyQt5
```
or

```bash
pip3 install PyQt5
```

## Files

PPTP_GUII.ui: GUI implementation using QT Design

PPTP_GUI.py: GUI logic in python

PPTP_ConfigTemplate.txt: Has configuration template that is needed for modifying PPTP_ConfigFile

## To run

Make sure to have all three files in the same directory.

```bash
sudo python3 PPTP_GUI.py
```