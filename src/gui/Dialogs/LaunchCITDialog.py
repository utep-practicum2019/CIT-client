import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from engine.Engine import Engine
from time import sleep
import threading
from engine.Connection.Connection import Connection
import logging


class LaunchCITDialog(Gtk.Dialog):
    def __init__(self, parent, process):
        Gtk.Dialog.__init__(self, "CIT Connection", parent, 0, (Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_resizable(False)
        self.process = process

        box = self.get_content_area()

        self.set_default_size(225, 100)
        self.box_main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)

        self.label = Gtk.Label("Launching CIT with default browser.")
        self.box_main.pack_start(self.label, True, True, 0)

        self.spinner = Gtk.Spinner()
        # self.spinner.start()
        self.box_main.pack_start(self.spinner, True, True, 0)

        self.box_spacer01 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.box_main.pack_start(self.box_spacer01, True, True, 0)

        self.box_status = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        self.statusLabel = Gtk.Label("Default browser will open within 10 secs.")
        self.box_status.pack_start(self.statusLabel, True, True, 0)
        self.box_main.pack_start(self.box_status, True, True, 0)

        self.get_widget_for_response(Gtk.ResponseType.OK).set_sensitive(True)

        box.pack_start(self.box_main, True, True, 0)

        self.show_all()

        # self.status = -1
        # t = threading.Thread(target=self.watchLaunchStatus())
        # t.start()

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

    def watchLaunchStatus(self):
        logging.debug("watchLaunchStatus(): instantiated")

        # self.setGUIStatus("Attempting Launch...", True, False)
        # count = 5
        # while count > 0:
        #     self.setGUIStatus("Attempting Launch..." + str(count), True, False)
        #     sleep(1)
        #     count -= 1
        # self.setGUIStatus("Launch successful.", False, True)

        # if self.process is None:
        #     logging.debug("watchLaunchStatus(): process is None. return")
        #     return
        #
        # will check status every half second and will either display attempting or success or fail
        # retVal = self.process.poll()
        # while retVal is None:
        #     logging.debug("watchLaunchStatus(): polling launch process")
        #     logging.debug("watchLaunchStatus(): retVal: " + str(retVal))
        #     if retVal is None:
        #         self.setGUIStatus("Attempting Launch...", True, False)
        #         logging.debug("watchLaunchStatus(): process running")
        #     elif retVal == 0:
        #         self.setGUIStatus("Launch successful.", False, True)
        #         logging.debug("watchLaunchStatus(): browser launch success")
        #     else:
        #         self.setGUIStatus("Launch failed.", False, True)
        #         logging.debug("watchLaunchStatus(): browser launch failure")
        #     sleep(1)
        #     retVal = self.process.poll()




        logging.debug("watchLaunchStatus(): thread ending")
