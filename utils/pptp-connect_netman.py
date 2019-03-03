#!/usr/bin/env python

from subprocess import Popen, PIPE, STDOUT
from sys import argv, platform
import logging
import shlex
import threading
import NetworkManager
from time import sleep

class Connection:
    
    def __init__(self, connectionName, serverIP):
        if platform == "linux" or platform == "linux2":
            self.POSIX = True
    
        self.connected = False
        self.connectionName = connectionName
        self.serverIP = serverIP
        self.p = None #will hold connection process

    def connectPPTP(self, username, password):
        logging.info("Using: " + username + "/"+password)
        if self.POSIX:
            logging.debug("Starting pptp connection thread")
            #test command is: 
            #pptpsetup --create pptpccaa --server 11.0.0.100 --username test3 --password test3 --encrypt --start
            connCmd = "pptpsetup --create " + self.connectionName + " --server " + self.serverIP + " --username " + username + " --password " + password + " --encrypt --start"
            self.t = threading.Thread(target=self.watchProcess, args=(connCmd,))
            self.t.start()

    def watchProcess(self, cmd):
        logging.debug("watchProcess(): initiated")
        #Function for starting the process and capturing its stdout
        try:
            logging.debug("Starting process: " + str(cmd) + "\r\n")
            #TODO: also check to make sure network manager is installed
            if self.POSIX:
                status = activateConnection(self.connectionName)
                if status == True:
                    self.connected = True
                    logging.debug("watchProcess(): connection successful")
                else:
                    logging.debug("watchProcess(): connection failed")
                    self.connected = False
            else:
                logging.error("Platform is not linux or linux2")
                print("Sorry your platform is not supported")

        except Exception as x:
            logging.error(" watchProcess(): Something went wrong while running process: " + str(cmd) + "\r\n" + str(x))
            if self.p != None and self.p.poll() == None:
                self.p.terminate()
                self.connected = False

    def disconnectPPTP(self):
        logging.debug(" checking if connection thread running " + str(self.connected) + " poll: " + str(self.p.poll()))
        if self.p != None and self.p.poll() == None:
            logging.debug(" thread is running, attempting to kill")
            self.p.terminate()
            logging.debug(" Thread state: " + str(self.p.poll()))
            self.connected = False
        else:
            logging.debug(" thread is not running")
            self.connected = False

def activateConnection(connectionName):
    logging.debug("activateConnection(): instantiated")
    # Find the connection
    name = connectionName
    connections = NetworkManager.Settings.ListConnections()
    connections = dict([(x.GetSettings()['connection']['id'], x) for x in connections])
    conn = connections[name]

    # Find a suitable device
    ctype = conn.GetSettings()['connection']['type']
    if ctype == 'vpn':
        for dev in NetworkManager.NetworkManager.GetDevices():
            if dev.State == NetworkManager.NM_DEVICE_STATE_ACTIVATED and dev.Managed:
                break
        else:
            logging.error("No active, managed device found")
            return 0
    else:
        dtype = {
            '802-11-wireless': NetworkManager.NM_DEVICE_TYPE_WIFI,
            '802-3-ethernet': NetworkManager.NM_DEVICE_TYPE_ETHERNET,
            'gsm': NetworkManager.NM_DEVICE_TYPE_MODEM,
        }.get(ctype, ctype)
        devices = NetworkManager.NetworkManager.GetDevices()

        for dev in devices:
            if dev.DeviceType == dtype and dev.State == NetworkManager.NM_DEVICE_STATE_DISCONNECTED:
                break
        else:
            logging.error("No suitable and available %s device found" % ctype)
            return 0

    # And connect
    NetworkManager.NetworkManager.ActivateConnection(conn, dev, "/")
    logging.info("Connection found and activation initiated")
    return 1

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Starting Program")
    #TODO: read from an XML file eventually
    connectionName = "VPN connection 4"
    serverIP = "11.0.0.100"
    conn = Connection(connectionName, serverIP)
    
    #TODO: read from a dialog box eventually
    #username = "test3"
    #password = "test3"

    username = argv[1]
    password = argv[2]
    logging.debug("Calling connectionPPTP()")
    conn.connectPPTP(username, password)
    while conn.connected == False:
        logging.debug("Connection not established")
        sleep(1)
#    sleep(3)
#    logging.debug("Calling disconnectPPTP()")
#    conn.disconnectPPTP()
    
#keywords/phraes to search for connection status:
#Connect: -> connecting
#Modem hangup -> hanging up
#Connection Terminated -> connection terminated
