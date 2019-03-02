import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from engine.Engine import Engine
from time import sleep
import threading
from engine.VMManage.VMManage import VMManage
import logging

class VMRetrieveDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "VM Retrieve Dialog", parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_resizable(False)
        box = self.get_content_area()

        self.set_default_size(225, 100)
        self.box_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)

        self.label = Gtk.Label("Virtual Machine Retrieval")
        self.box_main.pack_start(self.label, True, True, 0)

        self.spinner = Gtk.Spinner()
        self.spinner.start()
        self.box_main.pack_start(self.spinner, True, True, 0)
        
        self.box_spacer01 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.box_main.pack_start(self.box_spacer01, True, True, 0)

        self.box_status = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.statusLabel = Gtk.Label("Working...")
        self.box_status.pack_start(self.statusLabel, True, True, 0)
        self.box_main.pack_start(self.box_status, True, True, 0)

        self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(False)

        box.pack_start(self.box_main, True, True, 0)
        
        self.show_all()

        self.status = -1
        t = threading.Thread(target=self.retrieveStatus)
        t.start()
                
        
    def setGUIStatus(self, msg, spin, buttonEnabled):
        self.statusLabel.set_text(msg)
        if spin != None:
            if spin == True:
                self.spinner.start()
            else:
                self.spinner.stop()
        if buttonEnabled != None:
            if buttonEnabled == True:
                self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(True)
            else:
                self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(False)
        
    def retrieveStatus(self):
        logging.debug("watchRetrieveStatus(): instantiated")
        self.statusLabel.set_text("Querying VirtualBox Service...")
        e = Engine.getInstance()
        #execute refresh command
        logging.debug("watchRetrieveStatus(): running: vm-manage refresh")
        e.execute("vm-manage refresh")
        #will check status every 1 second until refresh command is finished
        while(True):        
            self.status = e.execute("vm-manage mgrstatus")
            logging.debug("watchRetrieveStatus(): result: " + str(self.status))
            if self.status["mgrStatus"]["readStatus"] != VMManage.MANAGER_IDLE or (self.status["mgrStatus"]["writeStatus"] != VMManage.MANAGER_IDLE and self.status["mgrStatus"]["writeStatus"] != VMManage.MANAGER_UNKNOWN):
                GLib.idle_add(self.setGUIStatus, "Reading VM Status", None, None)
            else:
                GLib.idle_add(self.setGUIStatus, "Retrieval Complete", False, True)
                break
            sleep(1)
        logging.debug("watchRetrieveStatus(): thread ending")
            
    def getFinalData(self):
        logging.debug("getFinalStatus(): initiated")
        logging.debug("getFinalStatus(): self.status: " + str(self.status))
        return self.status
