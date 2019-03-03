#!/usr/bin/env python

from subprocess import Popen, PIPE, STDOUT
from sys import argv, platform
import logging
import shlex
import threading
from time import sleep
import sys

class Connection:
    
    def __init__(self, connectionName, serverIP):
        if platform == "linux" or platform == "linux2":
            self.POSIX = True
    
        self.connStatus = False
        self.disConnStatus = False
        self.connectionName = connectionName
        self.serverIP = serverIP
        self.p = None #will hold connection process

    def connProcess(self, cmd):

        # Function for starting the process and capturing its stdout
        try:
            logging.debug("Starting process: " + str(cmd) + "\r\n")

            if self.POSIX:
                p = Popen(shlex.split(cmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
                self.connStatus = True
                while True:
                    out = p.stdout.read(1)
                    if out == '' and p.poll() != None:
                        break
                    if out != '':
                        sys.stdout.write(out)
                        sys.stdout.flush()

                logging.info("Process completed")
                self.connStatus = False
            else:
                logging.error("Platform is not linux or linux2")
                print("Sorry your platform is not supported")

        except Exception as x:
            logging.error(" connProcess(): Something went wrong while running process: " + str(cmd) + "\r\n" + str(x))
            if p != None and p.poll() == None:
                p.terminate()
                self.connStatus = False

    def disconnProcess(self, cmd):

        # Function for starting the process and capturing its stdout
        try:
            logging.debug("Starting process: " + str(cmd) + "\r\n")

            if self.POSIX:
                p = Popen(shlex.split(cmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
                self.disConnStatus = True
                while True:
                    out = p.stdout.read(1)
                    if out == '' and p.poll() != None:
                        break
                    if out != '':
                        sys.stdout.write(out)
                        sys.stdout.flush()

                logging.info("Process completed")
                self.disConnStatus = False
            else:
                logging.error("Platform is not linux or linux2")
                print("Sorry your platform is not supported")

        except Exception as x:
            logging.error(" disconnProcess(): Something went wrong while running process: " + str(cmd) + "\r\n" + str(x))
            if p != None and p.poll() == None:
                p.terminate()
                self.disConnStatus = False

    def connectPPTP(self, username, password):
        logging.info("Using: " + username + "/"+password)
        if self.POSIX:
            logging.debug("Starting pptp connection thread")
            #test command is: 
            #pptpsetup --create pptpccaa --server 11.0.0.100 --username test3 --password test3 --encrypt --start
            connCmd = "pptpsetup --create " + connectionName + " --server " + serverIP + " --username " + username + " --password " + password + " --encrypt --start"
            t = threading.Thread(target=self.connProcess, args=(connCmd,))
            t.start()

    def disconnectPPTP(self):
        logging.debug(" disconnectPPTP(): initiated")
        if self.POSIX:
            logging.debug("Shutting down pptp connection thread")
            #test command is:
            #pptpsetup --create pptpccaa --server 11.0.0.100 --username test3 --password test3 --encrypt --start
            closeConnCmd = "poff " + connectionName
            t = threading.Thread(target=self.disconnProcess, args=(closeConnCmd,))
            t.start()

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Starting Program")
    #TODO: read from an XML file eventually
    connectionName = "mypptp"
    serverIP = "11.0.0.100"
    conn = Connection(connectionName, serverIP)
    
    #TODO: read from a dialog box eventually
    #username = "test3"
    #password = "test3"

    username = argv[1]
    password = argv[2]
    for x in xrange(1,10):
        logging.debug("Calling connectionPPTP(): " + str(x))
        conn.connectPPTP(username, password)
        while conn.connStatus == False:
            logging.debug("Connection not established")
            sleep(1)
        sleep(3)
        logging.debug("Calling disconnectPPTP()")
        conn.disconnectPPTP()
        sleep(5)
    
#keywords/phraes to search for connection status:
#Connect: -> connecting
#Modem hangup -> hanging up
#Connection Terminated -> connection terminated
