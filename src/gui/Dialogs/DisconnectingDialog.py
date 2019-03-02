import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from engine.Engine import Engine
from time import sleep
import threading
from engine.Connection.Connection import Connection
import logging

class DisconnectingDialog(Gtk.Dialog):
    def __init__(self, parent, connName):
        Gtk.Dialog.__init__(self, "CIT Client Disconnecting", parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_resizable(False)
        self.connName = connName

        box = self.get_content_area()

        self.set_default_size(225, 100)
        self.box_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)

        self.label = Gtk.Label("Disconnecting from CIT")
        self.box_main.pack_start(self.label, True, True, 0)

        self.spinner = Gtk.Spinner()
        self.spinner.start()
        self.box_main.pack_start(self.spinner, True, True, 0)
        
        self.box_spacer01 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.box_main.pack_start(self.box_spacer01, True, True, 0)

        self.box_status = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.statusLabel = Gtk.Label("Initiating Disconnect...")
        self.box_status.pack_start(self.statusLabel, True, True, 0)
        self.box_main.pack_start(self.box_status, True, True, 0)

        self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(False)

        box.pack_start(self.box_main, True, True, 0)
        
        self.show_all()

        self.status = -1
        t = threading.Thread(target=self.watchDisconnStatus)
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
    
    def watchDisconnStatus(self):
        logging.debug("watchDisconnStatus(): instantiated")
        self.statusLabel.set_text("Checking connection")
        e = Engine.getInstance()
        #will check status every 1 second and will either display stopped or ongoing or connected
        while(True):
            logging.debug("watchDisconnStatus(): running: pptp status " + self.connName)
            self.status = e.execute("pptp status " + self.connName)
            logging.debug("watchConnStatus(): result: " + str(self.status))
            if self.status["connStatus"] == Connection.DISCONNECTING:
                GLib.idle_add(self.setGUIStatus, "Disconnecting...", None, None)
            elif self.status["connStatus"] == Connection.NOT_CONNECTED:
                GLib.idle_add(self.setGUIStatus, "Connection Disconnected.", False, True)
                break
            else:
                GLib.idle_add(self.setGUIStatus, "Could not disconnect", False, True)
                break
            sleep(1)
            
    def getFinalStatus(self):
        return self.status
