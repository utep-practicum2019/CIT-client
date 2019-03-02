#!/usr/bin/env python

from subprocess import Popen, PIPE
from Connection import Connection
from sys import argv, platform
import logging
import shlex
import threading
from time import sleep

class PPTPConnection(Connection):

    def __init__(self, connectionName):
        Connection.__init__(self, connectionName)

    def connProcess(self, cmd):

        # Function for starting the process and capturing its stdout
        try:
            logging.debug("Starting process: " + str(cmd) + "\r\n")
            localAddressSet = False
            remoteAddressSet = False
            if self.POSIX:
                p = Popen(shlex.split(cmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
                while True:
                    out = p.stdout.readline()
                    if out == '' and p.poll() != None:
                        break
                    if out != '':
                        logging.debug("connProcess(): stdout Line: " + out)
                        if "local  IP address " in out:
                            logging.debug("connProcess(): local IP address identified: " + out.strip().split("address ")[1])
                            self.localIPAddress = out.strip().split("address ")[1]
                            localAddressSet = True
                        if "remote IP address" in out:
                            logging.debug("connProcess(): remote IP address identified" + out.strip().split("address")[1])
                            remoteAddressSet = True
                            self.remoteIPAddress = out.strip().split("address ")[1]
                        if localAddressSet and remoteAddressSet:
                            logging.debug("connProcess(): Connection Established")
                            self.connStatus = Connection.CONNECTED
                logging.debug("connProcess(): Connection Closed")
                logging.info("Process completed: " + cmd)

                self.connStatus = Connection.NOT_CONNECTED
            else:
                logging.error("Platform is not linux or linux2")
                print("Sorry your platform is not supported")

        except Exception as x:
            logging.error(" connProcess(): Something went wrong while running process: " + str(cmd) + "\r\n" + str(x))
            self.disconnect()
            if p != None and p.poll() == None:
                p.terminate()

    def removeConnProcess(self, cmd):
        # Function for removing the process and capturing its stdout
        try:
            logging.debug("Starting process: " + str(cmd) + "\r\n")
            outlog = ""
            if self.POSIX:
                p = Popen(shlex.split(cmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
                while True:
                    out = p.stdout.readline()
                    if out == '' and p.poll() != None:
                        break
                    if out != '':
                        logging.debug("removeConnProcess(): stdout Line: " + out)

                logging.info("Process completed: " + cmd)
            else:
                logging.error("Platform is not linux or linux2")
                print("Sorry your platform is not supported")

        except Exception as x:
            logging.error(
                " removeConnProcess(): Something went wrong while running process: " + str(cmd) + "\r\n" + str(x))
            if p != None and p.poll() == None:
                p.terminate()

    def disconnProcess(self, cmd):
        # Function for starting the process and capturing its stdout
        try:
            logging.debug("Starting process: " + str(cmd) + "\r\n")
            outlog = ""
            if self.POSIX:
                p = Popen(shlex.split(cmd, posix=self.POSIX), stdout=PIPE, stderr=PIPE)
                while True:
                    out = p.stdout.readline()
                    if out == '' and p.poll() != None:
                        break
                    if out != '':
                        logging.debug("disconnProcess(): stdout Line: " + out)

                logging.info("Process completed: " + cmd)
                self.disConnStatus = Connection.NOT_DISCONNECTING

                self.connStatus = Connection.NOT_CONNECTED
                self.serverIP = None
                self.username = ""
                self.password = ""
                self.localIPAddress = ""
                self.serverIPAddress = ""
                #connectionName, serverIP, username, password

            else:
                logging.error("Platform is not linux or linux2")
                print("Sorry your platform is not supported")

        except Exception as x:
            logging.error(
                " disconnProcess(): Something went wrong while running process: " + str(cmd) + "\r\n" + str(x))
            if p != None and p.poll() == None:
                p.terminate()
                self.disConnStatus = Connection.NOT_DISCONNECTING

    def connect(self, serverIP, username, password):
        logging.info("Using: " + username + "/" + password)
        if self.POSIX:
            logging.debug("Starting pptp connection thread")
            self.connStatus = Connection.CONNECTING
            self.serverIP = serverIP
            # test command is:
            # pptpsetup --create pptpccaa --server 11.0.0.100 --username test3 --password test3 --encrypt --start
            connCmd = "timeout " + str(Connection.CONNECT_ATTEMPT_TIMEOUT_VAL) + " pptpsetup --create " + self.connectionName + " --server " + self.serverIP + " --username " + username + " --password " + password + " --encrypt --start"
            t = threading.Thread(target=self.connProcess, args=(connCmd,))
            t.start()

    def disconnect(self):
        logging.debug(" disconnect(): initiated")
        if self.POSIX:
            logging.debug("Shutting down pptp connection thread")
            self.connStatus = Connection.DISCONNECTING
            # test command is:
            # pptpsetup --create pptpccaa --server 11.0.0.100 --username test3 --password test3 --encrypt --start
            
            #remove the connection and then stop the connect (these can be done in parallel)
            removeConnCmd = "pptpsetup --delete " + self.connectionName
            t1 = threading.Thread(target=self.removeConnProcess, args=(removeConnCmd,))
            t1.start()
            
            closeConnCmd = "poff " + self.connectionName
            t2 = threading.Thread(target=self.disconnProcess, args=(closeConnCmd,))
            t2.start()

    def getStatus(self):
        logging.debug( "getStatus(): instantiated")
        #Don't want to rely on python objects in case we go with 3rd party clients in the future
        return {"connStatus" : self.connStatus, "disConnStatus" : self.disConnStatus, "connectionName" : self.connectionName, "serverIP" : self.serverIP, "localIP" : self.localIPAddress, "remoteIP" : self.remoteIPAddress}


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Starting Program")

    conn = PPTPConnection(connectionName = "testpptp")
    serverIP = "localhost"
    username = "test4"
    password = "test4"

    logging.debug("Calling connection()")
    conn.connect(serverIP, username, password)
    logging.debug("Status: " + str(conn.getStatus()))
    while conn.getStatus()["connStatus"] != Connection.CONNECTED:
        logging.debug("Connection not established, trying again in 5 seconds")
        sleep(5)
        if conn.getStatus()["connStatus"] == Connection.NOT_CONNECTED:
            conn.connect(serverIP, username, password)

    logging.debug("Status: " + str(conn.getStatus()))
    logging.debug("Calling disconnect()")
    conn.disconnect()
    sleep(5)
    logging.debug("Status: " + str(conn.getStatus()))
    logging.debug("Complete")

