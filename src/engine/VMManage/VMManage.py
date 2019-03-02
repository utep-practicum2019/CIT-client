#!/usr/bin/env python

from subprocess import Popen, PIPE
from sys import argv, platform
import logging
import shlex
import threading
from time import sleep

class VMManage:
    VM_SETUP_COMPLETE = 0
    VM_SETUP_NONE = 1
    VM_SETUP_UNKNOWN = -1
       
    MANAGER_READING = 7
    MANAGER_IDLE = 8
    MANAGER_WRITING = 9
    
    MANAGER_UNKNOWN = 10 
   
    MANAGER_STATUS_TIMEOUT_VAL = 11
   
    POSIX = False
    if platform == "linux" or platform == "linux2":
        POSIX = True
      
    def __init__(self):
        self.vms = {} #dict of VM()

    #abstractmethod
    def getManagerStatus(self):
        raise NotImplementedError()
    
    #abstractmethod
    def getVMStatus(self, vmName):
        raise NotImplementedError()

    #abstractmethod
    def refreshAllVMInfo(self):
        raise NotImplementedError()

    #abstractmethod
    def refreshVMInfo(self):
        raise NotImplementedError()

    #abstractmethod
    def startVM(self, vmName):
        raise NotImplementedError()

    def suspendVM(self, vmName):
        raise NotImplementedError()

    def stopVM(self, vmName):
        raise NotImplementedError()

    #abstractmethod
    def configureVM(self, VMName, srcIPAddress, dstIPAddress, srcPort, dstPort):
        raise NotImplementedError()

