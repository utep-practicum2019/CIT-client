#!/usr/bin/env python

import logging
import shlex
import argparse
import sys
from time import sleep
from Connection.Connection import Connection
from Connection.PPTPConnection import PPTPConnection
from Connection.PPTPConnectionWin import PPTPConnectionWin
from VMManage.VBoxManage import VBoxManage
from VMManage.VBoxManageWin import VBoxManageWin
import threading

class Engine:
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def getInstance(cls):
        logging.debug("getInstance() Engine: instantiated")
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
        return cls.__singleton_instance

    def __init__(self):
        #Virtually private constructor
        if Engine.__singleton_instance != None:
            raise Exception("Use the getInstance method to obtain an instance of this class")
        self.conns = {}
        self.configuredVM = ""
        if sys.platform == "linux" or sys.platform == "linux2":
            self.vmManage = VBoxManage()
        else:
            self.vmManage = VBoxManageWin()
        
        #build the parser
        self.buildParser()

    def pptpStatusCmd(self, args):
        logging.debug("pptpStatusCmd(): instantiated")
        return self.pptpGetStatus(args.connName)

    def pptpGetStatus(self, connName):
        if connName not in self.conns:
            logging.error("Connection does not exist or was not created through the engine")
            return -1
        #if we're good up to this point, run the command
        c = self.conns[connName]        
        return c.getStatus() # returns "connStatus" : self.connStatus, "disConnStatus" : self.disConnStatus, "refreshConnStatus" : self.refreshConnStatus, "connectionName" : self.connectionName, "serverIP" : self.serverIP, "localIP" : self.localIPAddress, "remoteIP" : self.remoteIPAddress

    def pptpForceRefreshConnStatusCmd(self, args):
        logging.debug("pptpForceRefreshConnStatusCmd(): instantiated")
        return self.pptpForceRefreshConnStatus(args.connName)

    def pptpForceRefreshConnStatus(self, connName):
        if connName not in self.conns:
            logging.error("Connection does not exist or was not created through the engine")
            return -1
        #if we're good up to this point, run the command
        c = self.conns[connName]
        logging.info("Got c: " + str(connName) + " : " + str(c) + " from " + str(self.conns))
        c.refresh()
        logging.info("PPTP force refresh connection status signal sent: " + connName)
        return 0

    def pptpStartCmd(self, args):
        logging.debug("pptpStartCmd(): instantiated")

        if args.connName not in self.conns:
            if sys.platform == "linux" or sys.platform == "linux2":
                c = PPTPConnection(connectionName = args.connName)
            else:
                c = PPTPConnectionWin(connectionName = args.connName)
            #have to add to list of conns because we don't know if the connection was successful until later
            self.conns[args.connName] = c
        else:
            c = self.conns[args.connName]
            logging.debug("PPTP connection exists, checking status")
            s = c.getStatus()["connStatus"]
            if s != Connection.NOT_CONNECTED:
                logging.error("PPTP connection status: " + str(s) + " connection busy")
                return -1
        #if we're good up to this point, attempt to connect
        c.connect(args.ipAddr, args.username, args.password)
        logging.info("PPTP connection signal sent: " + args.ipAddr + " " + args.username + " " + " " + args.password)
        return 0

    def pptpStopCmd(self, args):
        logging.debug("pptpStopCmd(): instantiated")
        if args.connName not in self.conns:
            logging.error("Connection does not exist or was not created through the engine")
            return -1
        else:
            c = self.conns[args.connName]
            logging.debug("PPTP connection exists, checking status")
            s = c.getStatus()["connStatus"]
            if s != Connection.CONNECTED:
                logging.error("PPTP connection status: " + str(s) + " not connected, try again later")
                return -1
        #if we're good up to this point, attempt to disconnect and then remove from list of known connections
        c.disconnect()
        logging.info("PPTP stop connection signal sent: " + args.connName)
        return 0

    def engineStatusCmd(self, args):
        logging.debug("engineStatusCmd(): instantiated")
        connsStatus = []
        vmsStatus = []

        for conn in self.conns:
            connsStatus.append("Connection: " + str(self.conns[conn].getStatus()))
            vmsStatus.append("VM: " + str(str(self.vmManage.getManagerStatus())))
        
        return "\r\nConnections: \r\n" + str(connsStatus) + "\r\nVMs:\r\n" + str(vmsStatus)


    def vmManageVMStatusCmd(self, args):
        logging.debug("vmManageStatusCmd(): instantiated")
        #will get the current configured VM (if any) display status
        vmName = "\""+args.vmName+"\""
        logging.debug("vmManageStatusCmd(): checking if vm is configured; stored: " + str(self.configuredVM))
        if self.configuredVM != vmName:          
            logging.error("VM has not been configured: " + str(vmName))
            return None
        logging.debug("Configured VM found, returning status")
        #self.vmManage.refreshAllVMInfo()
        return self.vmManage.getVMStatus(self.configuredVM)
            
    def vmManageMgrStatusCmd(self, args):
        return {"configuredVM" : self.configuredVM, "mgrStatus" : self.vmManage.getManagerStatus()}
        
    def vmManageRefreshCmd(self, args):
        self.vmManage.refreshAllVMInfo()
        
    def vmConfigCmd(self, args):
        logging.debug("vmConfigCmd(): instantiated")
        vmName = "\""+args.vmName+"\""
        #check if connection is present and is connected
        if args.connName not in self.conns:
            logging.error("vmConfigCmd(): connection name does not exist")
            return None
        else:
            c = self.conns[args.connName]
            logging.debug("vmConfigCmd(): PPTP connection exists, checking status")
            s = c.getStatus()["connStatus"]
            if s == Connection.NOT_CONNECTED or s == -1:
                logging.error("vmConfigCmd(): PPTP connection status: " + str(s) + " connection not established or does not exist")
                return None
                
        #check if vm exists
        logging.debug("vmConfigCmd(): Sending status request for VM: " + vmName)
        if self.vmManage.getVMStatus(vmName) == None:
            logging.error("vmConfigCmd(): vmName does not exist or you need to call refreshAllVMs: " + vmName)
            return None
        #if everything is good up to now, grab the last 3 of the IP address for ports, etc.
        #setup the vm with parameters: srcIP dstIP srcPort dstPort adaptor# connName
                
        #self.vmManage.configureVM(self, vmName, srcIPAddress, dstIPAddress, srcPort, dstPort, adaptorNum):
        logging.debug("vmConfigCmd(): VM found, configuring VM")
        self.vmManage.configureVM(vmName, args.srcIPAddress, args.dstIPAddress, args.srcPort, args.dstPort, args.adaptorNum)
        self.configuredVM = vmName
        
    def vmManageStartCmd(self, args):
        logging.debug("vmManageStartCmd(): instantiated")
        vmName = "\""+args.vmName+"\""
        if self.configuredVM != vmName:          
            logging.error("VM has not been configured")
            return None
        logging.debug("Configured VM found, starting vm")
        #send start command
        self.vmManage.startVM(vmName)

    def vmManageSuspendCmd(self, args):
        logging.debug("vmManageSuspendCmd(): instantiated")
        vmName = "\""+args.vmName+"\""
        if self.configuredVM != vmName:          
            logging.error("VM has not been configured")
            return None
        logging.debug("Configured VM found, suspending vm")
        #send start command
        self.vmManage.suspendVM(vmName)

    def buildParser(self):
        self.parser = argparse.ArgumentParser(description='Interface to the CIT client service.')
        self.subParsers = self.parser.add_subparsers()

        self.engineParser = self.subParsers.add_parser('engine', help='retrieve overall engine status')
        self.engineParser.add_argument('status', help='retrieve engine status')
        self.engineParser.set_defaults(func=self.engineStatusCmd)

# -----------Connection
        self.connectionParser = self.subParsers.add_parser('pptp')
        self.connectionSubParsers = self.connectionParser.add_subparsers(help='manage pptp connections')

    # -----------pptp
        self.pptpStatusParser = self.connectionSubParsers.add_parser('forcerefreshconnstatus', help='retrieve connection status')
        self.pptpStatusParser.add_argument('connName', metavar='<connection name>',
                                           help='name of connection to retrieve status')
        self.pptpStatusParser.set_defaults(func=self.pptpForceRefreshConnStatusCmd)

        self.pptpStatusParser = self.connectionSubParsers.add_parser('status', help='retrieve connection status (cached)')
        self.pptpStatusParser.add_argument('connName', metavar='<connection name>',
                                           help='name of connection to retrieve status')
        self.pptpStatusParser.set_defaults(func=self.pptpStatusCmd)

        self.pptpStartParser = self.connectionSubParsers.add_parser('start', help='start pptp connection')
        self.pptpStartParser.add_argument('connName', metavar='<connection name>', action="store",
                                          help='name of connection')
        self.pptpStartParser.add_argument('ipAddr', metavar='<ip address>', action="store",
                                          help='pptp server IPv4 address')
        self.pptpStartParser.add_argument('username', metavar='<username>', action="store",
                                          help='username for pptp connection')
        self.pptpStartParser.add_argument('password', metavar='<password>', action="store",
                                          help='password for pptp connection')
        self.pptpStartParser.set_defaults(func=self.pptpStartCmd)

        self.pptpStopParser = self.connectionSubParsers.add_parser('stop', help='stop an active pptp connection')
        self.pptpStopParser.add_argument('connName', metavar='<connection name>', action="store",
                                         help='name of connection to stop')
        self.pptpStopParser.set_defaults(func=self.pptpStopCmd)

#-----------VM Manage
        self.vmManageParser = self.subParsers.add_parser('vm-manage')
        self.vmManageSubParsers = self.vmManageParser.add_subparsers(help='manage vm')

        self.vmStatusParser = self.vmManageSubParsers.add_parser('vmstatus', help='retrieve vm status')
        self.vmStatusParser.add_argument('vmName', metavar='<vm name>', action="store",
                                           help='name of vm to retrieve status')
        self.vmStatusParser.set_defaults(func=self.vmManageVMStatusCmd)

        self.vmStatusParser = self.vmManageSubParsers.add_parser('mgrstatus', help='retrieve manager status')
        self.vmStatusParser.set_defaults(func=self.vmManageMgrStatusCmd)

        self.vmRefreshParser = self.vmManageSubParsers.add_parser('refresh', help='retreive current vm information')
        self.vmRefreshParser.set_defaults(func=self.vmManageRefreshCmd)

        self.vmConfigParser = self.vmManageSubParsers.add_parser('config', help='configure vm to connect to CIT')
        self.vmConfigParser.add_argument('vmName', metavar='<vm name>', action="store",
                                          help='name vm to configure')
        self.vmConfigParser.add_argument('srcIPAddress', metavar='<source ip address>', action="store",
                                          help='source IP used for UDP Tunnel')
        self.vmConfigParser.add_argument('dstIPAddress', metavar='<destination ip address>', action="store",
                                          help='destination IP used for UDP Tunnel')
        self.vmConfigParser.add_argument('srcPort', metavar='<source port>', action="store",
                                          help='source port used for UDP Tunnel')
        self.vmConfigParser.add_argument('dstPort', metavar='<destination port>', action="store",
                                          help='destination port used for UDP Tunnel')
        self.vmConfigParser.add_argument('adaptorNum', metavar='<adaptor number>', action="store",
                                          help='adaptor to use for UDP Tunnel configuration')
        self.vmConfigParser.add_argument('connName', metavar='<connection name>', action="store",
                                          help='connection to associate to configured VM')
        self.vmConfigParser.set_defaults(func=self.vmConfigCmd)

        self.vmStartParser = self.vmManageSubParsers.add_parser('start', help='start a vm')
        self.vmStartParser.add_argument('vmName', metavar='<vm name>', action="store",
                                          help='name of vm to start')
        self.vmStartParser.set_defaults(func=self.vmManageStartCmd)

        self.vmSuspendParser = self.vmManageSubParsers.add_parser('suspend', help='suspend a vm')
        self.vmSuspendParser.add_argument('vmName', metavar='<vm name>', action="store",
                                         help='name of vm to suspend')
        self.vmSuspendParser.set_defaults(func=self.vmManageSuspendCmd)

    def execute(self, cmd):
        logging.debug("execute(): instantiated")
        try:
            #parse out the command
            logging.debug("execute(): Received: " + str(cmd))
            r = self.parser.parse_args(shlex.split(cmd))
            #r = self.parser.parse_args(cmd)
            logging.debug("execute(): returning result: " + str(r))
            return r.func(r)
            
        except argparse.ArgumentError, exc:
            logging.error(exc.message, '\n', exc.argument)	
        except SystemExit:
            return

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("Starting Program")
###Base Engine tests
    logging.debug("Instantiating Engine")
    e = Engine()
    logging.debug("engine object: " + str(e))

    logging.debug("Calling Engine.getInstance()")
    e = Engine.getInstance()
    logging.debug("engine object: " + str(e))

    logging.debug("Calling Engine.getInstance()")
    e = Engine.getInstance()
    logging.debug("engine object: " + str(e))

###PPTP tests
	#error should occur
    e.execute("pptp start mypptp")
    res = e.execute("pptp status mypptp")
    
    sleep(1)
    #e.execute(sys.argv[1:])
    e.execute("pptp start mypptp localhost test4 test4")
    
    #now check status
    sleep(5)
    res = e.execute("pptp status mypptp")
    print "STATUS: " + str(res)
    localIP = res["localIP"]
    remoteIP = res["remoteIP"]
    
    if localIP == "":
        logging.error("Connection unsuccessful, quiting")
        exit()


    sleep(1)
    res = e.execute("engine status")
    print "ENGINE STATUS: " + str(res)

    res = e.execute("pptp status mypptp")
    print "STATUS: " + str(res)

###VMManage tests
    sleep(5)
    #Check status without refresh
    res = e.execute("vm-manage vmstatus \"ubuntu-core4.7\"")
    print "VM-Manage Status of ubuntu-core4.7: " + str(res)

    #Refresh
    sleep(5)
    res = e.execute("vm-manage refresh")
    print "Refreshing" + str(res)

    #get parameters needed to setup VM for UDPTunnel
    octetLocal = localIP.split(".")[3]
    octetRemote = remoteIP.split(".")[3]

    #try to setup with a vm that doesn't exist
    sleep(8)
    res = e.execute("vm-manage config \"NoVM\" "+localIP+" " + remoteIP + " " +octetLocal + " " + octetLocal + " 1 mypptp")  

    #try to setup with a connection that doesn't exist
    sleep(5)
    res = e.execute("vm-manage config \"NoVM\" "+localIP+" " + remoteIP + " " +octetLocal + " " + octetLocal + " 1 mypptp1")
    
    #setup the vm with parameters: srcIP dstIP srcPort dstPort adaptor# connName
    sleep(1)
    res = e.execute("vm-manage config \"ubuntu-core4.7\" "+localIP+" " + remoteIP + " " +octetLocal + " " + octetLocal + " 1 mypptp")
    print "Called vm config: " + str(res)
    
    #Refresh
    sleep(1)
    res = e.execute("vm-manage refresh")
    print "Refreshing" + str(res)

    #Check status of vm
    sleep(5)
    res = e.execute("vm-manage vmstatus \"ubuntu-core4.7\"")
    print "VM-Manage Status of ubuntu-core4.7 " + str(res)

    #Check status of manager
    sleep(5)
    res = e.execute("vm-manage mgrstatus")
    print "VM-Manage Status " + str(res)

    sleep(1)
    res = e.execute("pptp stop mypptp")
    print "STATUS: " + str(res)
