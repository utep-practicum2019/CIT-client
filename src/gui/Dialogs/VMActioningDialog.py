import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from engine.Engine import Engine
from time import sleep
import threading
from engine.VMManage.VMManage import VMManage
import logging

class VMActioningDialog(Gtk.Dialog):
    def __init__(self, parent, vmName, vmAction):
        Gtk.Dialog.__init__(self, "Executing VM Action", parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_resizable(False)
        self.vmName = vmName
        self.vmAction = vmAction

        box = self.get_content_area()

        self.set_size_request(225, 100)
        self.box_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)

        self.label = Gtk.Label("Executing VM Action")
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
        t = threading.Thread(target=self.vmActionStatus)
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
        
    def vmActionStatus(self):
        logging.debug("vmActionStatus(): instantiated")
        
        self.statusLabel.set_text("Executing " + self.vmAction + " on VM: " + self.vmName + "...")
        e = Engine.getInstance()
        #execute refresh command
        logging.debug("vmActionStatus(): running: vm-manage " + self.vmAction + " " + self.vmName )
        e.execute("vm-manage " + self.vmAction + " " + self.vmName)
        #will check status every 1 second until refresh command is finished
        while(True):        
            self.status = e.execute("vm-manage mgrstatus")
            logging.debug("vmActionStatus(): result: " + str(self.status))
            if self.status["mgrStatus"]["readStatus"] != VMManage.MANAGER_IDLE or (self.status["mgrStatus"]["writeStatus"] != VMManage.MANAGER_IDLE and self.status["mgrStatus"]["writeStatus"] != VMManage.MANAGER_UNKNOWN):
                GLib.idle_add(self.setGUIStatus, "Executing VM " + self.vmAction + "...", None, None)
            else:
                GLib.idle_add(self.setGUIStatus, "Complete", False, True)
                break
            sleep(1)
        logging.debug("configureStatus(): thread ending")
            
    def getFinalStatus(self):
        logging.debug("getFinalStatus(): initiated")
        logging.debug("getFinalStatus(): self.status: " + str(self.status))
        return self.status
