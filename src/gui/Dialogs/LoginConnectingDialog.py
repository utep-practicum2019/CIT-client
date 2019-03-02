import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from engine.Engine import Engine
from time import sleep
import threading
from engine.Connection.Connection import Connection
import logging

class LoginConnectingDialog(Gtk.Dialog):
    def __init__(self, parent, connName):
        Gtk.Dialog.__init__(self, "CIT Connection", parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_resizable(False)
        self.connName = connName

        box = self.get_content_area()

        self.set_default_size(225, 100)
        self.box_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)

        self.label = Gtk.Label("Connecting to the CIT")
        self.box_main.pack_start(self.label, True, True, 0)

        self.spinner = Gtk.Spinner()
        self.spinner.start()
        self.box_main.pack_start(self.spinner, True, True, 0)
        
        self.box_spacer01 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.box_main.pack_start(self.box_spacer01, True, True, 0)

        self.box_status = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.statusLabel = Gtk.Label("Attempting to connect...")
        self.box_status.pack_start(self.statusLabel, True, True, 0)
        self.box_main.pack_start(self.box_status, True, True, 0)

        self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(False)

        box.pack_start(self.box_main, True, True, 0)
        
        self.show_all()

        self.status = -1
        t = threading.Thread(target=self.watchConnStatus)
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
        
    def watchConnStatus(self):
        logging.debug("watchConnStatus(): instantiated")
        self.statusLabel.set_text("Checking connection")
        e = Engine.getInstance()
        #will check status every 1 second and will either display stopped or ongoing or connected
        while(True):
            logging.debug("watchConnStatus(): running: pptp status " + self.connName)
            self.status = e.execute("pptp status " + self.connName)
            logging.debug("watchConnStatus(): result: " + str(self.status))
            if self.status["connStatus"] == Connection.CONNECTING:
                GLib.idle_add(self.setGUIStatus, "Trying to establish connection", None, None)
            elif self.status["connStatus"] == Connection.CONNECTED:
                GLib.idle_add(self.setGUIStatus, "Connection Established", False, True)
                break
            else:
                GLib.idle_add(self.setGUIStatus, "Could not connect", False, True)
                break
            sleep(1)
        logging.debug("watchConnStatus(): thread ending")
            
    def getFinalStatus(self):
        logging.debug("getFinalStatus(): initiated")
        logging.debug("getFinalStatus(): self.status: " + str(self.status))
        return self.status
